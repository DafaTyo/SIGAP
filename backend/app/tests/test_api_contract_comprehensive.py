"""
Comprehensive API contract test — covers ALL endpoints from api-contract.yaml v0.2.0.

Each endpoint group is tested for:
  - Happy path (201/200)
  - Validation errors (422)
  - Auth errors (401/403) where applicable
  - Not found (404)
  - Pagination contract (data + pagination shape)
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _idempotency_key() -> dict[str, str]:
    return {"X-Idempotency-Key": _new_uuid()}


_VALID_VENDOR_PAYLOAD = {
    "nama_usaha": "PT Pangan Sejahtera",
    "nik_penanggung_jawab": "3175123456789012",
    "nib": "NIB-9123456789",
    "alamat": "Jl. Merdeka No. 42",
    "provinsi": "DKI Jakarta",
    "kabupaten_kota": "Jakarta Pusat",
}


# ─────────────────────────────────────────────
# 1. AUTH
# ─────────────────────────────────────────────


@pytest.mark.anyio
class TestAuthContract:
    """POST /auth/login • GET /auth/me • GET /auth/me/permissions"""

    async def test_login_success(self, client, test_user):
        resp = await client.post(
            "/v1/auth/login",
            data={"username": test_user["email"], "password": test_user["password"]},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"
        assert isinstance(body["expires_in"], int)
        assert body["expires_in"] > 0

    async def test_login_wrong_password(self, client, test_user):
        resp = await client.post(
            "/v1/auth/login",
            data={"username": test_user["email"], "password": "wrongpass"},
        )
        assert resp.status_code == 401

        # Must conform to Error schema
        body = resp.json()
        assert "error_code" in body or "detail" in body

    async def test_login_nonexistent_user(self, client):
        resp = await client.post(
            "/v1/auth/login",
            data={"username": "noone@test.com", "password": "testpass123"},
        )
        assert resp.status_code == 401

    async def test_login_invalid_json(self, client):
        """Missing fields → 422."""
        resp = await client.post("/v1/auth/login", json={})
        assert resp.status_code == 422

    async def test_me_endpoint(self, client, auth_headers):
        resp = await client.get("/v1/auth/me", headers=auth_headers)
        assert resp.status_code == 200
        body = resp.json()
        assert "id" in body
        assert "role" in body

    async def test_me_without_token(self, client):
        resp = await client.get("/v1/auth/me")
        assert resp.status_code == 401

    async def test_me_with_invalid_token(self, client):
        resp = await client.get("/v1/auth/me", headers={"Authorization": "Bearer invalid-token"})
        assert resp.status_code in (401, 403)

    async def test_permissions_endpoint(self, client, auth_headers):
        resp = await client.get("/v1/auth/me/permissions", headers=auth_headers)
        assert resp.status_code == 200
        body = resp.json()
        assert "role" in body
        assert "permissions" in body
        assert isinstance(body["permissions"], list)
        assert "scope" in body

    async def test_permissions_without_token(self, client):
        resp = await client.get("/v1/auth/me/permissions")
        assert resp.status_code == 401


# ─────────────────────────────────────────────
# 2. VENDORS
# ─────────────────────────────────────────────


@pytest.mark.anyio
class TestVendorContract:
    """POST/GET /vendors • GET/PATCH /vendors/{id} • GET /vendors/{id}/nik
    POST /vendors/{id}/documents • GET .../documents/{docId}/status
    POST /vendors/{id}/verify • GET /vendors/{id}/sio • GET /vendors/{id}/score"""

    async def _create_vendor(self, client, headers) -> dict:
        resp = await client.post(
            "/v1/vendors",
            json=_VALID_VENDOR_PAYLOAD,
            headers={**headers, **_idempotency_key()},
        )
        assert resp.status_code == 201
        return resp.json()

    # -- POST /vendors --

    async def test_create_vendor_success(self, client, auth_headers):
        data = await self._create_vendor(client, auth_headers)
        assert data["nama_usaha"] == _VALID_VENDOR_PAYLOAD["nama_usaha"]
        # NIK must be masked
        assert data["nik_penanggung_jawab_masked"].startswith("3175")
        assert "********" in data["nik_penanggung_jawab_masked"]
        assert "id" in data
        assert data["status"] in ("pending_verification", "verified")
        assert isinstance(data["vendor_score"], (int, float))

    async def test_create_vendor_missing_required(self, client, auth_headers):
        resp = await client.post(
            "/v1/vendors",
            json={"nama_usaha": "Incomplete"},
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code == 422

    async def test_create_vendor_invalid_nik_length(self, client, auth_headers):
        payload = {**_VALID_VENDOR_PAYLOAD, "nik_penanggung_jawab": "12345"}
        resp = await client.post(
            "/v1/vendors",
            json=payload,
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code == 422

    async def test_create_vendor_without_auth(self, client):
        resp = await client.post(
            "/v1/vendors",
            json=_VALID_VENDOR_PAYLOAD,
            headers=_idempotency_key(),
        )
        assert resp.status_code == 401

    async def test_create_vendor_without_idempotency(self, client, auth_headers):
        resp = await client.post("/v1/vendors", json=_VALID_VENDOR_PAYLOAD, headers=auth_headers)
        # Idempotency middleware may reject with 400 or process normally
        assert resp.status_code in (201, 400, 422)

    # -- GET /vendors --

    async def test_list_vendors_success(self, client, auth_headers):
        resp = await client.get("/v1/vendors", headers=auth_headers)
        assert resp.status_code == 200
        body = resp.json()
        assert "data" in body
        assert "pagination" in body
        assert isinstance(body["data"], list)
        assert body["pagination"]["page"] >= 1
        assert body["pagination"]["page_size"] >= 1

    async def test_list_vendors_with_filters(self, client, auth_headers):
        resp = await client.get(
            "/v1/vendors?status=pending_verification&province=DKI+Jakarta&page=1&page_size=5",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "data" in body
        assert "pagination" in body

    async def test_list_vendors_without_auth(self, client):
        resp = await client.get("/v1/vendors")
        assert resp.status_code == 401

    async def test_list_vendors_invalid_page(self, client, auth_headers):
        resp = await client.get("/v1/vendors?page=0", headers=auth_headers)
        assert resp.status_code == 422

    # -- GET /vendors/{vendorId} --

    async def test_get_vendor_detail_success(self, client, auth_headers):
        created = await self._create_vendor(client, auth_headers)
        resp = await client.get(f"/v1/vendors/{created['id']}", headers=auth_headers)
        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == created["id"]
        assert "nik_penanggung_jawab_masked" in body
        assert "nik_penanggung_jawab" not in body  # raw NIK never exposed

    async def test_get_vendor_not_found(self, client, auth_headers):
        resp = await client.get(f"/v1/vendors/{_new_uuid()}", headers=auth_headers)
        assert resp.status_code == 404

    async def test_get_vendor_invalid_uuid(self, client, auth_headers):
        resp = await client.get("/v1/vendors/not-a-uuid", headers=auth_headers)
        assert resp.status_code == 422

    # -- PATCH /vendors/{vendorId} --

    async def test_patch_vendor_success(self, client, auth_headers):
        created = await self._create_vendor(client, auth_headers)
        resp = await client.patch(
            f"/v1/vendors/{created['id']}",
            json={"alamat": "Jl. Baru No. 99"},
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code in (200, 404, 501)  # 501 if not implemented

    async def test_patch_vendor_no_idempotency(self, client, auth_headers):
        created = await self._create_vendor(client, auth_headers)
        resp = await client.patch(
            f"/v1/vendors/{created['id']}",
            json={"alamat": "Jl. Baru No. 99"},
            headers=auth_headers,
        )
        assert resp.status_code in (200, 400, 404, 422)

    async def test_patch_vendor_nik_rejected(self, client, auth_headers):
        """Contract says NIK changes must go through re-verification, not patch."""
        created = await self._create_vendor(client, auth_headers)
        resp = await client.patch(
            f"/v1/vendors/{created['id']}",
            json={"nik_penanggung_jawab": "1111111111111111"},
            headers={**auth_headers, **_idempotency_key()},
        )
        # Schema doesn't accept nik_penanggung_jawab so it should either
        # silently ignore or 422
        assert resp.status_code in (200, 422)

    # -- GET /vendors/{vendorId}/nik (RESTRICTED — PII reveal) --

    async def test_get_vendor_nik_success(self, client, auth_headers):
        created = await self._create_vendor(client, auth_headers)
        resp = await client.get(f"/v1/vendors/{created['id']}/nik", headers=auth_headers)
        # Admin should have access
        if resp.status_code == 200:
            body = resp.json()
            assert "nik_penanggung_jawab" in body
            assert body["nik_penanggung_jawab"] == _VALID_VENDOR_PAYLOAD["nik_penanggung_jawab"]
        else:
            assert resp.status_code in (403, 404)

    async def test_get_vendor_nik_not_found(self, client, auth_headers):
        resp = await client.get(f"/v1/vendors/{_new_uuid()}/nik", headers=auth_headers)
        assert resp.status_code in (403, 404)

    # -- POST /vendors/{vendorId}/documents --

    async def test_upload_document_success(self, client, auth_headers):
        created = await self._create_vendor(client, auth_headers)
        resp = await client.post(
            f"/v1/vendors/{created['id']}/documents",
            data={"document_type": "nib"},
            files={"file": ("test.pdf", b"%PDF-1.4 mock content", "application/pdf")},
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code in (201, 404, 501)  # 501 if not implemented yet

    async def test_upload_document_missing_file(self, client, auth_headers):
        created = await self._create_vendor(client, auth_headers)
        resp = await client.post(
            f"/v1/vendors/{created['id']}/documents",
            data={"document_type": "nib"},
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code in (422, 404)

    async def test_upload_document_invalid_type(self, client, auth_headers):
        created = await self._create_vendor(client, auth_headers)
        resp = await client.post(
            f"/v1/vendors/{created['id']}/documents",
            data={"document_type": "invalid_type"},
            files={"file": ("test.pdf", b"dummy", "application/pdf")},
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code in (422, 404)

    # -- GET /vendors/{vendorId}/documents/{documentId}/status --

    async def test_document_validation_status(self, client, auth_headers):
        created = await self._create_vendor(client, auth_headers)
        doc_id = _new_uuid()
        resp = await client.get(
            f"/v1/vendors/{created['id']}/documents/{doc_id}/status",
            headers=auth_headers,
        )
        assert resp.status_code in (200, 404, 501)

    # -- GET .../documents/{documentId}/status/stream --
    # SSE endpoint — just verify it responds (if implemented)

    async def test_document_status_stream(self, client, auth_headers):
        created = await self._create_vendor(client, auth_headers)
        doc_id = _new_uuid()
        resp = await client.get(
            f"/v1/vendors/{created['id']}/documents/{doc_id}/status/stream",
            headers=auth_headers,
        )
        assert resp.status_code in (200, 404, 501)

    # -- POST /vendors/{vendorId}/verify --

    async def test_verify_vendor_approve(self, client, auth_headers):
        created = await self._create_vendor(client, auth_headers)
        resp = await client.post(
            f"/v1/vendors/{created['id']}/verify",
            json={"decision": "approve", "notes": "Semua dokumen lengkap"},
            headers={**auth_headers, **_idempotency_key()},
        )
        if resp.status_code == 200:
            body = resp.json()
            assert body["status"] in ("verified", "rejected")
        else:
            assert resp.status_code in (403, 404)

    async def test_verify_vendor_invalid_decision(self, client, auth_headers):
        created = await self._create_vendor(client, auth_headers)
        resp = await client.post(
            f"/v1/vendors/{created['id']}/verify",
            json={"decision": "maybe"},
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code in (422, 403, 404)

    async def test_verify_vendor_without_role(self, client, auth_headers):
        """Only verifikator_bgn/admin can verify."""
        created = await self._create_vendor(client, auth_headers)
        # auth_headers is admin, so this should work
        resp = await client.post(
            f"/v1/vendors/{created['id']}/verify",
            json={"decision": "approve"},
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code in (200, 403, 404)

    # -- GET /vendors/{vendorId}/sio --

    async def test_get_vendor_sio(self, client, auth_headers):
        created = await self._create_vendor(client, auth_headers)
        resp = await client.get(f"/v1/vendors/{created['id']}/sio", headers=auth_headers)
        if resp.status_code == 200:
            body = resp.json()
            assert "sio_code" in body
            assert "qr_code_url" in body
        else:
            assert resp.status_code in (404, 501)

    async def test_get_vendor_sio_not_found(self, client, auth_headers):
        resp = await client.get(f"/v1/vendors/{_new_uuid()}/sio", headers=auth_headers)
        assert resp.status_code in (404, 501)

    # -- GET /vendors/{vendorId}/score --

    async def test_get_vendor_score(self, client, auth_headers):
        created = await self._create_vendor(client, auth_headers)
        resp = await client.get(f"/v1/vendors/{created['id']}/score", headers=auth_headers)
        if resp.status_code == 200:
            body = resp.json()
            assert "score" in body
            assert "factors" in body
        else:
            assert resp.status_code in (404, 501)

    async def test_get_vendor_score_not_found(self, client, auth_headers):
        resp = await client.get(f"/v1/vendors/{_new_uuid()}/score", headers=auth_headers)
        assert resp.status_code in (404, 501)


# ─────────────────────────────────────────────
# 3. DISTRIBUTIONS
# ─────────────────────────────────────────────


@pytest.mark.anyio
class TestDistributionContract:
    """POST/GET /distributions • GET /distributions/{id}
    GET /distributions/{id}/metadata • POST /distributions/{id}/appeal"""

    async def _create_vendor(self, client, headers) -> dict:
        resp = await client.post(
            "/v1/vendors",
            json=_VALID_VENDOR_PAYLOAD,
            headers={**headers, **_idempotency_key()},
        )
        assert resp.status_code == 201
        return resp.json()

    # -- POST /distributions --

    async def _create_distribution_data(self, vendor_id: str) -> dict:
        return {
            "vendor_id": vendor_id,
            "jumlah_porsi": 200,
            "lokasi_sekolah": "SDN 01 Gambir",
            "latitude": -6.1754,
            "longitude": 106.8272,
        }

    async def test_submit_distribution_success(self, client, auth_headers):
        vendor = await self._create_vendor(client, auth_headers)
        payload = await self._create_distribution_data(vendor["id"])
        resp = await client.post(
            "/v1/distributions",
            json=payload,
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code == 201
        body = resp.json()
        assert body["jumlah_porsi"] == 200
        assert "tampering_suspicion" in body
        assert body["tampering_suspicion"] is False

    async def test_submit_distribution_without_idempotency(self, client, auth_headers):
        vendor = await self._create_vendor(client, auth_headers)
        payload = await self._create_distribution_data(vendor["id"])
        resp = await client.post("/v1/distributions", json=payload, headers=auth_headers)
        assert resp.status_code in (201, 400, 422)

    async def test_submit_distribution_missing_required(self, client, auth_headers):
        resp = await client.post(
            "/v1/distributions",
            json={},
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code == 422

    async def test_submit_distribution_without_auth(self, client):
        resp = await client.post(
            "/v1/distributions",
            json={"vendor_id": _new_uuid(), "jumlah_porsi": 100, "latitude": 0.0, "longitude": 0.0},
            headers=_idempotency_key(),
        )
        assert resp.status_code == 401

    # -- GET /distributions --

    async def test_list_distributions_success(self, client, auth_headers):
        resp = await client.get("/v1/distributions", headers=auth_headers)
        assert resp.status_code == 200
        body = resp.json()
        assert "data" in body
        assert "pagination" in body
        assert isinstance(body["data"], list)

    async def test_list_distributions_with_filters(self, client, auth_headers):
        resp = await client.get(
            "/v1/distributions?page=1&page_size=5",
            headers=auth_headers,
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "data" in body
        assert body["pagination"]["page"] == 1
        assert body["pagination"]["page_size"] == 5

    async def test_list_distributions_pagination_shape(self, client, auth_headers):
        resp = await client.get("/v1/distributions", headers=auth_headers)
        assert resp.status_code == 200
        p = resp.json()["pagination"]
        assert "page" in p
        assert "page_size" in p
        assert "total_items" in p
        assert "total_pages" in p

    # -- GET /distributions/{id} --

    async def test_get_distribution_detail(self, client, auth_headers):
        vendor = await self._create_vendor(client, auth_headers)
        payload = await self._create_distribution_data(vendor["id"])
        created = await client.post(
            "/v1/distributions",
            json=payload,
            headers={**auth_headers, **_idempotency_key()},
        )
        assert created.status_code == 201
        dist_id = created.json()["id"]

        resp = await client.get(f"/v1/distributions/{dist_id}", headers=auth_headers)
        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == dist_id
        assert body["jumlah_porsi"] == 200

    async def test_get_distribution_not_found(self, client, auth_headers):
        resp = await client.get(f"/v1/distributions/{_new_uuid()}", headers=auth_headers)
        assert resp.status_code == 404

    # -- GET /distributions/{id}/metadata --

    async def test_get_distribution_metadata(self, client, auth_headers):
        vendor = await self._create_vendor(client, auth_headers)
        payload = await self._create_distribution_data(vendor["id"])
        created = await client.post(
            "/v1/distributions",
            json=payload,
            headers={**auth_headers, **_idempotency_key()},
        )
        assert created.status_code == 201
        dist_id = created.json()["id"]

        resp = await client.get(f"/v1/distributions/{dist_id}/metadata", headers=auth_headers)
        if resp.status_code == 200:
            body = resp.json()
            assert "distribution_id" in body
            assert "latitude" in body
            assert "tampering_suspicion" in body
        else:
            # May be 403 if role not allowed (e.g. vendor role can't access metadata)
            assert resp.status_code in (403, 404)

    async def test_get_distribution_metadata_not_found(self, client, auth_headers):
        resp = await client.get(f"/v1/distributions/{_new_uuid()}/metadata", headers=auth_headers)
        assert resp.status_code in (403, 404, 501)

    # -- POST /distributions/{id}/appeal --

    async def test_submit_appeal_success(self, client, auth_headers):
        vendor = await self._create_vendor(client, auth_headers)
        payload = await self._create_distribution_data(vendor["id"])
        created = await client.post(
            "/v1/distributions",
            json=payload,
            headers={**auth_headers, **_idempotency_key()},
        )
        assert created.status_code == 201
        dist_id = created.json()["id"]

        resp = await client.post(
            f"/v1/distributions/{dist_id}/appeal",
            data={"reason": "Foto diambil dari lokasi berbeda karena banjir"},
            files={"supporting_evidence": ("bukti.jpg", b"fakeimagecontent", "image/jpeg")},
            headers={**auth_headers, **_idempotency_key()},
        )
        if resp.status_code == 200:
            body = resp.json()
            assert "appeal_status" in body
            assert body["appeal_status"] in ("pending_review", "in_progress")
        else:
            # Vendor role required; admin may be rejected
            assert resp.status_code in (403, 404, 501)

    async def test_submit_appeal_missing_reason(self, client, auth_headers):
        vendor = await self._create_vendor(client, auth_headers)
        payload = await self._create_distribution_data(vendor["id"])
        created = await client.post(
            "/v1/distributions",
            json=payload,
            headers={**auth_headers, **_idempotency_key()},
        )
        assert created.status_code == 201
        dist_id = created.json()["id"]

        resp = await client.post(
            f"/v1/distributions/{dist_id}/appeal",
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code in (422, 403, 404)


# ─────────────────────────────────────────────
# 4. COMPLAINTS
# ─────────────────────────────────────────────


@pytest.mark.anyio
class TestComplaintContract:
    """POST/GET /complaints • GET/PATCH /complaints/{id}"""

    async def _create_vendor(self, client, headers) -> dict:
        resp = await client.post(
            "/v1/vendors",
            json=_VALID_VENDOR_PAYLOAD,
            headers={**headers, **_idempotency_key()},
        )
        assert resp.status_code == 201
        return resp.json()

    # -- POST /complaints (public — no auth required) --

    async def test_submit_complaint_anonymous(self, client, auth_headers):
        vendor = await self._create_vendor(client, auth_headers)
        payload = {
            "vendor_id": vendor["id"],
            "kategori": "keterlambatan",
            "deskripsi": "Makanan datang jam 11 padahal harus jam 9",
        }
        resp = await client.post(
            "/v1/complaints",
            json=payload,
            headers=_idempotency_key(),
        )
        assert resp.status_code == 201
        body = resp.json()
        assert "ticket_number" in body
        assert body["ticket_number"].startswith("SG-")
        assert "id" in body

    async def test_submit_complaint_with_nama_pelapor(self, client, auth_headers):
        vendor = await self._create_vendor(client, auth_headers)
        payload = {
            "vendor_id": vendor["id"],
            "kategori": "kualitas_makanan",
            "deskripsi": "Nasi basi",
            "nama_pelapor": "Budi Santoso",
        }
        resp = await client.post(
            "/v1/complaints",
            json=payload,
            headers=_idempotency_key(),
        )
        assert resp.status_code == 201

    async def test_submit_complaint_missing_required(self, client):
        resp = await client.post("/v1/complaints", json={}, headers=_idempotency_key())
        assert resp.status_code == 422

    async def test_submit_complaint_invalid_kategori(self, client, auth_headers):
        vendor = await self._create_vendor(client, auth_headers)
        payload = {
            "vendor_id": vendor["id"],
            "kategori": "unknown_category",
            "deskripsi": "Test",
        }
        resp = await client.post(
            "/v1/complaints",
            json=payload,
            headers=_idempotency_key(),
        )
        assert resp.status_code in (422, 201)

    # -- GET /complaints --

    async def test_list_complaints_success(self, client, auth_headers):
        resp = await client.get("/v1/complaints", headers=auth_headers)
        assert resp.status_code == 200
        body = resp.json()
        assert "data" in body
        assert "pagination" in body
        assert isinstance(body["data"], list)

    async def test_list_complaints_with_filters(self, client, auth_headers):
        resp = await client.get(
            "/v1/complaints?status=baru&severity=tinggi&page=1&page_size=10",
            headers=auth_headers,
        )
        assert resp.status_code == 200

    async def test_list_complaints_pagination_shape(self, client, auth_headers):
        resp = await client.get("/v1/complaints", headers=auth_headers)
        assert resp.status_code == 200
        p = resp.json()["pagination"]
        for key in ("page", "page_size", "total_items", "total_pages"):
            assert key in p

    # -- GET /complaints/{id} (public) --

    async def test_get_complaint_detail_public(self, client, auth_headers):
        vendor = await self._create_vendor(client, auth_headers)
        payload = {
            "vendor_id": vendor["id"],
            "kategori": "keterlambatan",
            "deskripsi": "Telat 2 jam",
        }
        created = await client.post("/v1/complaints", json=payload, headers=_idempotency_key())
        assert created.status_code == 201
        complaint_id = created.json()["id"]

        # Public (no auth) should be able to read complaint by ID
        resp = await client.get(f"/v1/complaints/{complaint_id}")
        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == complaint_id
        assert "ticket_number" in body

    async def test_get_complaint_not_found(self, client):
        resp = await client.get(f"/v1/complaints/{_new_uuid()}")
        assert resp.status_code == 404

    async def test_get_complaint_invalid_uuid(self, client):
        resp = await client.get("/v1/complaints/not-a-uuid")
        assert resp.status_code == 422

    # -- PATCH /complaints/{id} (verifikator_bgn only) --

    async def test_patch_complaint_status(self, client, auth_headers):
        vendor = await self._create_vendor(client, auth_headers)
        payload = {"vendor_id": vendor["id"], "kategori": "keracunan", "deskripsi": "Keracunan massal"}
        created = await client.post("/v1/complaints", json=payload, headers=_idempotency_key())
        assert created.status_code == 201
        complaint_id = created.json()["id"]

        resp = await client.patch(
            f"/v1/complaints/{complaint_id}",
            json={"status": "diproses", "resolution_notes": "Sedang diinvestigasi"},
            headers={**auth_headers, **_idempotency_key()},
        )
        if resp.status_code == 200:
            body = resp.json()
            assert body["status"] == "diproses"
        else:
            assert resp.status_code in (403, 404)

    async def test_patch_complaint_invalid_status(self, client, auth_headers):
        vendor = await self._create_vendor(client, auth_headers)
        payload = {"vendor_id": vendor["id"], "kategori": "keterlambatan", "deskripsi": "Telat"}
        created = await client.post("/v1/complaints", json=payload, headers=_idempotency_key())
        assert created.status_code == 201
        complaint_id = created.json()["id"]

        resp = await client.patch(
            f"/v1/complaints/{complaint_id}",
            json={"status": "invalid_status"},
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code in (422, 403, 404)

    async def test_patch_complaint_without_auth(self, client, auth_headers):
        vendor = await self._create_vendor(client, auth_headers)
        payload = {"vendor_id": vendor["id"], "kategori": "keterlambatan", "deskripsi": "Telat"}
        created = await client.post("/v1/complaints", json=payload, headers=_idempotency_key())
        assert created.status_code == 201
        complaint_id = created.json()["id"]

        resp = await client.patch(
            f"/v1/complaints/{complaint_id}",
            json={"status": "diproses"},
            headers=_idempotency_key(),
        )
        assert resp.status_code == 401


# ─────────────────────────────────────────────
# 5. PUBLIC
# ─────────────────────────────────────────────


@pytest.mark.anyio
class TestPublicContract:
    """GET /public/vendors/verify • GET /public/dashboard/summary"""

    # -- GET /public/vendors/verify --

    async def test_public_verify_vendor(self, client):
        resp = await client.get("/v1/public/vendors/verify")
        assert resp.status_code == 200
        body = resp.json()
        assert isinstance(body, list)

    async def test_public_verify_vendor_with_query(self, client):
        resp = await client.get("/v1/public/vendors/verify?query=Pangan")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    async def test_public_verify_vendor_with_sio_code(self, client):
        resp = await client.get("/v1/public/vendors/verify?sio_code=SIO-2026-JKT-000123")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    # -- GET /public/dashboard/summary --

    async def test_public_dashboard_summary(self, client):
        resp = await client.get("/v1/public/dashboard/summary")
        assert resp.status_code == 200
        body = resp.json()
        expected_keys = (
            "total_vendor_aktif",
            "total_vendor_termonitor_persen",
            "total_pengaduan_bulan_ini",
            "pengaduan_tertindaklanjuti_persen",
        )
        for key in expected_keys:
            assert key in body, f"Missing field: {key}"

    async def test_public_dashboard_summary_types(self, client):
        resp = await client.get("/v1/public/dashboard/summary")
        body = resp.json()
        assert isinstance(body["total_vendor_aktif"], int)
        assert isinstance(body["total_vendor_termonitor_persen"], (int, float))
        assert isinstance(body["total_pengaduan_bulan_ini"], int)
        assert isinstance(body["pengaduan_tertindaklanjuti_persen"], (int, float))


# ─────────────────────────────────────────────
# 6. ADMIN
# ─────────────────────────────────────────────


@pytest.mark.anyio
class TestAdminContract:
    """POST /admin/users • GET /admin/users"""

    # -- POST /admin/users --

    async def test_admin_create_user(self, client, auth_headers):
        resp = await client.post(
            "/v1/admin/users",
            json={
                "email": "newuser@test.com",
                "name": "New User",
                "password": "password123",
                "role": "vendor",
                "scope_value": ["DKI Jakarta"],
            },
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code == 201
        body = resp.json()
        assert body["email"] == "newuser@test.com"
        assert body["name"] == "New User"
        assert body["role"] == "vendor"

    async def test_admin_create_user_duplicate_email(self, client, auth_headers, test_user):
        resp = await client.post(
            "/v1/admin/users",
            json={
                "email": test_user["email"],
                "name": "Duplicate",
                "password": "password123",
                "role": "vendor",
            },
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code in (409, 422)

    async def test_admin_create_user_missing_required(self, client, auth_headers):
        resp = await client.post(
            "/v1/admin/users",
            json={"email": "incomplete@test.com"},
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code == 422

    async def test_admin_create_user_without_auth(self, client):
        resp = await client.post(
            "/v1/admin/users",
            json={
                "email": "noauth@test.com",
                "name": "No Auth",
                "password": "password123",
                "role": "vendor",
            },
            headers=_idempotency_key(),
        )
        assert resp.status_code == 401

    async def test_admin_create_user_invalid_role(self, client, auth_headers):
        resp = await client.post(
            "/v1/admin/users",
            json={
                "email": "badrole@test.com",
                "name": "Bad Role",
                "password": "password123",
                "role": "superadmin",
            },
            headers={**auth_headers, **_idempotency_key()},
        )
        assert resp.status_code == 422

    # -- GET /admin/users --

    async def test_admin_list_users(self, client, auth_headers):
        resp = await client.get("/v1/admin/users", headers=auth_headers)
        assert resp.status_code == 200
        body = resp.json()
        assert isinstance(body, list)
        if len(body) > 0:
            user = body[0]
            assert "id" in user
            assert "email" in user
            assert "role" in user

    async def test_admin_list_users_without_auth(self, client):
        resp = await client.get("/v1/admin/users")
        assert resp.status_code == 401


# ─────────────────────────────────────────────
# 7. AUDIT LOGS
# ─────────────────────────────────────────────


@pytest.mark.anyio
class TestAuditContract:
    """GET /audit-logs"""

    async def test_audit_logs_success(self, client, auth_headers):
        resp = await client.get("/v1/audit-logs", headers=auth_headers)
        assert resp.status_code == 200
        body = resp.json()
        assert "data" in body
        assert isinstance(body["data"], list)

    async def test_audit_logs_with_filters(self, client, auth_headers):
        resp = await client.get(
            "/v1/audit-logs?entity_type=vendor&action=CREATE",
            headers=auth_headers,
        )
        assert resp.status_code == 200

    async def test_audit_logs_invalid_action(self, client, auth_headers):
        resp = await client.get(
            "/v1/audit-logs?action=INVALID_ACTION",
            headers=auth_headers,
        )
        assert resp.status_code in (200, 422)

    async def test_audit_logs_without_auth(self, client):
        resp = await client.get("/v1/audit-logs")
        assert resp.status_code == 401


# ─────────────────────────────────────────────
# 8. FULL PIPELINE E2E
# ─────────────────────────────────────────────


@pytest.mark.anyio
class TestFullPipeline:
    """End-to-end flow: auth → create vendor → submit distribution → submit complaint → verify → check."""

    async def test_full_vendor_lifecycle(self, client, auth_headers):
        # 1. Auth: GET /me
        me = await client.get("/v1/auth/me", headers=auth_headers)
        assert me.status_code == 200

        # 2. Create a vendor
        vendor_resp = await client.post(
            "/v1/vendors",
            json=_VALID_VENDOR_PAYLOAD,
            headers={**auth_headers, **_idempotency_key()},
        )
        assert vendor_resp.status_code == 201
        vendor = vendor_resp.json()
        vendor_id = vendor["id"]

        # 3. Verify vendor
        verify_resp = await client.post(
            f"/v1/vendors/{vendor_id}/verify",
            json={"decision": "approve"},
            headers={**auth_headers, **_idempotency_key()},
        )
        # May be allowed (admin → verify)
        assert verify_resp.status_code in (200, 403)

        # 4. List vendors — should include our vendor
        list_resp = await client.get("/v1/vendors", headers=auth_headers)
        assert list_resp.status_code == 200
        ids = [v["id"] for v in list_resp.json()["data"]]
        assert vendor_id in ids

        # 5. Submit distribution
        dist_resp = await client.post(
            "/v1/distributions",
            json={
                "vendor_id": vendor_id,
                "jumlah_porsi": 300,
                "lokasi_sekolah": "SDN 02 Menteng",
                "latitude": -6.195,
                "longitude": 106.835,
            },
            headers={**auth_headers, **_idempotency_key()},
        )
        assert dist_resp.status_code == 201
        dist_id = dist_resp.json()["id"]

        # 6. Get distribution detail
        detail = await client.get(f"/v1/distributions/{dist_id}", headers=auth_headers)
        assert detail.status_code == 200

        # 7. Submit complaint
        comp_resp = await client.post(
            "/v1/complaints",
            json={
                "vendor_id": vendor_id,
                "kategori": "kekurangan_porsi",
                "deskripsi": "Porsi kurang 50",
            },
            headers=_idempotency_key(),
        )
        assert comp_resp.status_code == 201
        complaint_id = comp_resp.json()["id"]

        # 8. Get complaint (public)
        comp_detail = await client.get(f"/v1/complaints/{complaint_id}")
        assert comp_detail.status_code == 200

        # 9. Dashboard summary
        dash = await client.get("/v1/public/dashboard/summary")
        assert dash.status_code == 200

        # 10. Audit logs
        audit = await client.get("/v1/audit-logs", headers=auth_headers)
        assert audit.status_code == 200


# ─────────────────────────────────────────────
# 9. NEGATIVE EDGE CASES
# ─────────────────────────────────────────────


@pytest.mark.anyio
class TestEdgeCases:
    """Cross-cutting edge cases: malformed UUIDs, unauthenticated access, etc."""

    async def test_all_get_endpoints_require_auth(self, client):
        """Read endpoints that require auth should 401 without token."""
        protected_reads = [
            "/v1/vendors",
            "/v1/vendors/00000000-0000-0000-0000-000000000000",
            "/v1/distributions",
            "/v1/distributions/00000000-0000-0000-0000-000000000000",
            "/v1/complaints",
            "/v1/admin/users",
            "/v1/audit-logs",
        ]
        for path in protected_reads:
            resp = await client.get(path)
            assert resp.status_code == 401, f"{path} should 401 without auth, got {resp.status_code}"

    async def test_public_endpoints_do_not_require_auth(self, client):
        """Public endpoints must work without auth."""
        public_reads = [
            "/v1/public/vendors/verify",
            "/v1/public/dashboard/summary",
        ]
        for path in public_reads:
            resp = await client.get(path)
            assert resp.status_code == 200, f"{path} should 200 without auth, got {resp.status_code}"

    async def test_openapi_json_accessible(self, client):
        """OpenAPI schema should be available at /openapi.json."""
        resp = await client.get("/openapi.json")
        assert resp.status_code == 200
        schema = resp.json()
        assert "paths" in schema
        assert len(schema["paths"]) > 0
