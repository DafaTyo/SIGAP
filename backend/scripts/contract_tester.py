#!/usr/bin/env python3
"""Contract Tester — standalone smoke test untuk ALL endpoints di api-contract.yaml v0.2.0.

Usage:
    # Default: http://localhost:8000
    python scripts/contract_tester.py

    # Custom URL:
    python scripts/contract_tester.py --base-url https://api.sigap.example.id/v1

    # With auth credentials:
    python scripts/contract_tester.py --email admin@sigap.gov --password rahasia

    # Only specific tag(s):
    python scripts/contract_tester.py --tags Auth,Vendor

    # JSON report:
    python scripts/contract_tester.py --report result.json

Requires: pip install httpx pyyaml
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

import httpx
import yaml

# ── Config ──────────────────────────────────────────────────────────────────

HERE = Path(__file__).resolve().parent
API_CONTRACT = HERE.parent / "api-contract.yaml"

BASE_URL = "http://localhost:8000/v1"

def _unique_vendor() -> dict:
    """Return vendor payload with unique nama_usaha to avoid UNIQUE constraint clash."""
    suffix = uuid.uuid4().hex[:8]
    return {
        "nama_usaha": f"PT Pangan Sejahtera {suffix}",
        "nik_penanggung_jawab": "3175123456789012",
        "nib": f"NIB-{suffix}",
        "alamat": "Jl. Merdeka No. 42",
        "provinsi": "DKI Jakarta",
        "kabupaten_kota": "Jakarta Pusat",
    }


VALID_VENDOR = _unique_vendor()

VALID_LOGIN = {"username": "admin@sigap.gov", "password": "admin123"}


# ── Results ─────────────────────────────────────────────────────────────────


@dataclass
class Result:
    endpoint: str
    method: str
    status: str  # PASS | FAIL | SKIP
    expected: str = ""
    actual: str = ""
    detail: str = ""
    duration_ms: float = 0.0


results: list[Result] = []
_fail_count = 0


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _ik() -> dict[str, str]:
    return {"X-Idempotency-Key": _new_uuid()}


# ── Reporter ────────────────────────────────────────────────────────────────


def report(endpoint: str, method: str, status: str, **kw: Any) -> None:
    r = Result(endpoint=endpoint, method=method, status=status, **kw)
    results.append(r)
    global _fail_count
    emoji = {"PASS": "✓", "FAIL": "✗", "SKIP": "—", "INFO": "·"}
    print(f"  {emoji.get(status, '?')} [{status}] {method} {endpoint}" +
          (f"  ({kw.get('detail', '')})" if kw.get("detail") else "") +
          (f"  got={kw.get('actual', '')}" if kw.get("actual") else ""))
    if status == "FAIL":
        _fail_count += 1


def print_summary() -> None:
    total = len(results)
    passed = sum(1 for r in results if r.status == "PASS")
    failed = sum(1 for r in results if r.status == "FAIL")
    skipped = sum(1 for r in results if r.status == "SKIP")
    infos = sum(1 for r in results if r.status == "INFO")
    print(f"\n{'='*60}")
    print(f"  TOTAL : {total}")
    print(f"  PASS  : {passed}")
    print(f"  FAIL  : {failed}")
    print(f"  SKIP  : {skipped}")
    print(f"  INFO  : {infos}")
    if failed:
        print(f"\n  FAILED ENDPOINTS:")
        for r in results:
            if r.status == "FAIL":
                print(f"    ✗ {r.method} {r.endpoint}")
                print(f"      Expected: {r.expected}")
                print(f"      Actual:   {r.actual}")
                if r.detail:
                    print(f"      Detail:   {r.detail}")
    print(f"{'='*60}")


def save_report(path: str) -> None:
    data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "summary": {
            "total": len(results),
            "pass": sum(1 for r in results if r.status == "PASS"),
            "fail": sum(1 for r in results if r.status == "FAIL"),
            "skip": sum(1 for r in results if r.status == "SKIP"),
        },
        "results": [asdict(r) for r in results],
    }
    Path(path).write_text(json.dumps(data, indent=2))
    print(f"\nReport saved: {path}")


# ── Assert helpers ──────────────────────────────────────────────────────────


def _assert(
    endpoint: str,
    method: str,
    resp: httpx.Response,
    *,
    expected_status: int | list[int],
    check_json_key: str | None = None,
    check_json_keys: list[str] | None = None,
    fail_detail: str = "",
    start: float = 0.0,
) -> bool:
    elapsed = (time.time() - start) * 1000
    expected_list = [expected_status] if isinstance(expected_status, int) else expected_status
    ok = resp.status_code in expected_list
    detail = fail_detail or ""
    actual = f"{resp.status_code} {resp.reason_phrase}"

    # Check JSON key presence for PASS cases
    body = {}
    if ok and (check_json_key or check_json_keys):
        try:
            body = resp.json()
        except Exception:
            ok = False
            detail = "Response not valid JSON"
            actual = resp.text[:200]

    if ok and check_json_key:
        if check_json_key not in body:
            ok = False
            detail = f"Missing key '{check_json_key}' in response body"
            actual = json.dumps(body)[:200]

    if ok and check_json_keys:
        missing = [k for k in check_json_keys if k not in body]
        if missing:
            ok = False
            detail = f"Missing keys: {missing}"
            actual = json.dumps(body)[:200]

    status = "PASS" if ok else "FAIL"
    report(
        endpoint, method, status,
        expected=str(expected_list),
        actual=actual,
        detail=detail,
        duration_ms=round(elapsed, 1),
    )
    return ok


# ── Test runner ─────────────────────────────────────────────────────────────


class ContractTester:
    def __init__(self, base_url: str, email: str, password: str, tags: list[str] | None):
        self.base = base_url.rstrip("/")
        self.client = httpx.Client(timeout=30.0, follow_redirects=False)
        self.token: str | None = None
        self.auth_headers: dict[str, str] = {}
        self.email = email
        self.password = password
        self.tags = [t.strip().lower() for t in tags] if tags else None

    def _should_run(self, endpoint_tags: list[str]) -> bool:
        if self.tags is None:
            return True
        return any(t.lower() in self.tags for t in endpoint_tags)

    def _url(self, path: str) -> str:
        return f"{self.base}{path}"

    # ── Auth ──────────────────────────────────────────────────────────────

    def test_auth_login(self) -> bool:
        ok = True
        start = time.time()
        resp = self.client.post(
            self._url("/auth/login"),
            data={"username": self.email, "password": self.password},
        )
        ok &= _assert("/auth/login", "POST", resp, expected_status=200,
                       check_json_key="access_token", start=start)
        if resp.status_code == 200:
            self.token = resp.json()["access_token"]
            self.auth_headers = {"Authorization": f"Bearer {self.token}"}

        # Wrong password
        start = time.time()
        resp2 = self.client.post(
            self._url("/auth/login"),
            data={"username": self.email, "password": "wrong_password"},
        )
        ok &= _assert("/auth/login", "POST", resp2, expected_status=401,
                       fail_detail="wrong password should 401", start=start)
        return ok

    def test_auth_me(self) -> bool:
        if not self.token:
            report("/auth/me", "GET", "SKIP", detail="no token")
            return False
        ok = True
        resp = self.client.get(self._url("/auth/me"), headers=self.auth_headers)
        ok &= _assert("/auth/me", "GET", resp, expected_status=200,
                       check_json_keys=["id", "role"])
        # Without auth
        resp2 = self.client.get(self._url("/auth/me"))
        ok &= _assert("/auth/me", "GET", resp2, expected_status=401,
                       fail_detail="no auth should 401")
        return ok

    def test_auth_permissions(self) -> bool:
        if not self.token:
            report("/auth/me/permissions", "GET", "SKIP", detail="no token")
            return False
        ok = True
        resp = self.client.get(self._url("/auth/me/permissions"), headers=self.auth_headers)
        ok &= _assert("/auth/me/permissions", "GET", resp, expected_status=200,
                       check_json_keys=["role", "permissions", "scope"])
        return ok

    # ── Vendors ───────────────────────────────────────────────────────────

    def _create_vendor(self) -> dict | None:
        resp = self.client.post(
            self._url("/vendors"),
            json=VALID_VENDOR,
            headers={**self.auth_headers, **_ik()},
        )
        if resp.status_code == 201:
            return resp.json()
        return None

    def test_vendor_crud(self) -> bool:
        if not self.token:
            for ep in ["/vendors", "/vendors/{id}", "/vendors/{id}/nik",
                        "/vendors/{id}/documents", "/vendors/{id}/verify",
                        "/vendors/{id}/sio", "/vendors/{id}/score"]:
                report(ep, "POST/GET", "SKIP", detail="no token")
            return False
        ok = True

        # POST /vendors
        start = time.time()
        r1 = self.client.post(
            self._url("/vendors"), json=VALID_VENDOR,
            headers={**self.auth_headers, **_ik()},
        )
        ok &= _assert("/vendors", "POST", r1, expected_status=201,
                       check_json_keys=["id", "nama_usaha", "status"],
                       start=start)
        vendor_id = r1.json().get("id") if r1.status_code == 201 else None
        if not vendor_id:
            report("/vendors", "POST", "FAIL", detail="cannot create vendor")
            return ok

        # POST /vendors with missing fields → 422
        start = time.time()
        r1b = self.client.post(
            self._url("/vendors"), json={"nama_usaha": "Incomplete"},
            headers={**self.auth_headers, **_ik()},
        )
        ok &= _assert("/vendors", "POST", r1b, expected_status=422,
                       fail_detail="missing required fields", start=start)

        # GET /vendors
        start = time.time()
        r2 = self.client.get(self._url("/vendors"), headers=self.auth_headers)
        ok &= _assert("/vendors", "GET", r2, expected_status=200,
                       check_json_keys=["data", "pagination"], start=start)

        # GET /vendors with filters
        r2b = self.client.get(
            self._url("/vendors?status=pending_verification&page=1&page_size=5"),
            headers=self.auth_headers,
        )
        ok &= _assert("/vendors", "GET", r2b, expected_status=200, start=start)

        # GET /vendors/{vendorId}
        start = time.time()
        r3 = self.client.get(self._url(f"/vendors/{vendor_id}"), headers=self.auth_headers)
        ok &= _assert(f"/vendors/{vendor_id}", "GET", r3, expected_status=200,
                       check_json_keys=["id", "nama_usaha"], start=start)
        # Not found
        r3b = self.client.get(self._url(f"/vendors/{_new_uuid()}"), headers=self.auth_headers)
        ok &= _assert(f"/vendors/{_new_uuid()[:8]}...", "GET", r3b, expected_status=404,
                       fail_detail="not found")

        # PATCH /vendors/{vendorId}
        start = time.time()
        r4 = self.client.patch(
            self._url(f"/vendors/{vendor_id}"), json={"alamat": "Jl. Baru No. 99"},
            headers={**self.auth_headers, **_ik()},
        )
        ok &= _assert(f"/vendors/{vendor_id}", "PATCH", r4, expected_status=200,
                       check_json_key="alamat", start=start)

        # GET /vendors/{vendorId}/nik
        start = time.time()
        r5 = self.client.get(self._url(f"/vendors/{vendor_id}/nik"), headers=self.auth_headers)
        ok &= _assert(f"/vendors/{vendor_id}/nik", "GET", r5, expected_status=[200, 403],
                       start=start)

        # POST /vendors/{vendorId}/documents
        start = time.time()
        r6 = self.client.post(
            self._url(f"/vendors/{vendor_id}/documents"),
            data={"document_type": "nib"},
            files={"file": ("test.pdf", b"%PDF-1.4 mock content", "application/pdf")},
            headers={**self.auth_headers, **_ik()},
        )
        ok &= _assert(f"/vendors/{vendor_id}/documents", "POST", r6, expected_status=201,
                       start=start)

        # GET /vendors/{vendorId}/documents/{documentId}/status
        doc_id = _new_uuid()
        r7 = self.client.get(
            self._url(f"/vendors/{vendor_id}/documents/{doc_id}/status"),
            headers=self.auth_headers,
        )
        ok &= _assert(
            f"/vendors/{vendor_id}/documents/{doc_id[:8]}/status",
            "GET", r7, expected_status=[200, 404, 501], start=time.time(),
        )

        # GET .../status/stream (SSE)
        r7b = self.client.get(
            self._url(f"/vendors/{vendor_id}/documents/{doc_id}/status/stream"),
            headers=self.auth_headers,
        )
        ok &= _assert(
            f"/vendors/{vendor_id}/documents/{doc_id[:8]}/status/stream",
            "GET", r7b, expected_status=[200, 404, 501], start=time.time(),
        )

        # POST /vendors/{vendorId}/verify
        r8 = self.client.post(
            self._url(f"/vendors/{vendor_id}/verify"),
            json={"decision": "approve", "notes": "Lengkap"},
            headers={**self.auth_headers, **_ik()},
        )
        ok &= _assert(
            f"/vendors/{vendor_id}/verify", "POST", r8,
            expected_status=[200, 403], start=time.time(),
        )

        # GET /vendors/{vendorId}/sio
        r9 = self.client.get(self._url(f"/vendors/{vendor_id}/sio"), headers=self.auth_headers)
        ok &= _assert(
            f"/vendors/{vendor_id}/sio", "GET", r9,
            expected_status=[200, 404, 501], start=time.time(),
        )

        # GET /vendors/{vendorId}/score
        r10 = self.client.get(self._url(f"/vendors/{vendor_id}/score"), headers=self.auth_headers)
        ok &= _assert(
            f"/vendors/{vendor_id}/score", "GET", r10,
            expected_status=[200, 404, 501], start=time.time(),
        )

        return ok

    # ── Distributions ─────────────────────────────────────────────────────

    def test_distributions(self, vendor_id: str | None) -> bool:
        if not self.token:
            for ep in ["/distributions", "/distributions/{id}",
                        "/distributions/{id}/metadata", "/distributions/{id}/appeal"]:
                report(ep, "POST/GET", "SKIP", detail="no token")
            return False
        if not vendor_id:
            report("(vendor required)", "distributions", "SKIP", detail="no vendor")
            return False
        ok = True

        # POST /distributions
        dist_payload = {
            "vendor_id": vendor_id,
            "jumlah_porsi": 200,
            "lokasi_sekolah": "SDN 01 Gambir",
            "latitude": -6.1754,
            "longitude": 106.8272,
        }
        start = time.time()
        r1 = self.client.post(
            self._url("/distributions"), json=dist_payload,
            headers={**self.auth_headers, **_ik()},
        )
        ok &= _assert("/distributions", "POST", r1, expected_status=201,
                       check_json_keys=["id", "jumlah_porsi", "tampering_suspicion"],
                       start=start)
        dist_id = r1.json().get("id") if r1.status_code == 201 else None

        # GET /distributions
        r2 = self.client.get(self._url("/distributions"), headers=self.auth_headers)
        ok &= _assert("/distributions", "GET", r2, expected_status=200,
                       check_json_keys=["data", "pagination"])

        if dist_id:
            # GET /distributions/{id}
            r3 = self.client.get(self._url(f"/distributions/{dist_id}"), headers=self.auth_headers)
            ok &= _assert(f"/distributions/{dist_id}", "GET", r3, expected_status=200,
                           check_json_keys=["id", "jumlah_porsi"])

            # GET /distributions/{id}/metadata
            r4 = self.client.get(
                self._url(f"/distributions/{dist_id}/metadata"), headers=self.auth_headers,
            )
            ok &= _assert(
                f"/distributions/{dist_id}/metadata", "GET", r4,
                expected_status=[200, 403, 404], start=time.time(),
            )

            # POST /distributions/{id}/appeal
            r5 = self.client.post(
                self._url(f"/distributions/{dist_id}/appeal"),
                data={"reason": "Banjir, foto dari lokasi alternatif"},
                files={"supporting_evidence": ("bukti.jpg", b"fake", "image/jpeg")},
                headers={**self.auth_headers, **_ik()},
            )
            ok &= _assert(
                f"/distributions/{dist_id}/appeal", "POST", r5,
                expected_status=[200, 403, 404, 501], start=time.time(),
            )

        return ok

    # ── Complaints ────────────────────────────────────────────────────────

    def test_complaints(self, vendor_id: str | None) -> bool:
        ok = True

        comp_payload = {
            "vendor_id": vendor_id or _new_uuid(),
            "kategori": "keterlambatan",
            "deskripsi": "Makanan datang jam 11 padahal harus jam 9",
        }

        # POST /complaints (public)
        start = time.time()
        r1 = self.client.post(
            self._url("/complaints"), json=comp_payload, headers=_ik(),
        )
        ok &= _assert("/complaints", "POST", r1, expected_status=201,
                       check_json_keys=["id", "ticket_number"], start=start)
        complaint_id = r1.json().get("id") if r1.status_code == 201 else None

        # POST /complaints with nama_pelapor
        r1b = self.client.post(
            self._url("/complaints"),
            json={**comp_payload, "nama_pelapor": "Budi Santoso"},
            headers=_ik(),
        )
        ok &= _assert("/complaints", "POST", r1b, expected_status=201, start=time.time())

        # POST /complaints missing required → 422
        start = time.time()
        r1c = self.client.post(self._url("/complaints"), json={}, headers=_ik())
        ok &= _assert("/complaints", "POST", r1c, expected_status=422,
                       fail_detail="missing required fields", start=start)

        # GET /complaints (auth required)
        if self.token:
            r2 = self.client.get(self._url("/complaints"), headers=self.auth_headers)
            ok &= _assert("/complaints", "GET", r2, expected_status=200,
                           check_json_keys=["data", "pagination"])
        else:
            report("/complaints", "GET", "SKIP", detail="no token")

        if complaint_id:
            # GET /complaints/{id} (public — no auth)
            start = time.time()
            r3 = self.client.get(self._url(f"/complaints/{complaint_id}"))
            ok &= _assert(f"/complaints/{complaint_id}", "GET", r3, expected_status=200,
                           check_json_keys=["id", "ticket_number"], start=start)

            # PATCH /complaints/{id} (auth required)
            if self.token:
                start = time.time()
                r4 = self.client.patch(
                    self._url(f"/complaints/{complaint_id}"),
                    json={"status": "diproses", "resolution_notes": "Diinvestigasi"},
                    headers={**self.auth_headers, **_ik()},
                )
                ok &= _assert(
                    f"/complaints/{complaint_id}", "PATCH", r4,
                    expected_status=[200, 403, 404], start=time.time(),
                )
            else:
                report(f"/complaints/{complaint_id}", "PATCH", "SKIP", detail="no token")

            # GET /complaints/{id} not found
            r3b = self.client.get(self._url(f"/complaints/{_new_uuid()}"))
            ok &= _assert(f"/complaints/{_new_uuid()[:8]}...", "GET", r3b,
                           expected_status=404, fail_detail="not found")

        return ok

    # ── Public ────────────────────────────────────────────────────────────

    def test_public(self) -> bool:
        ok = True

        # GET /public/vendors/verify
        r1 = self.client.get(self._url("/public/vendors/verify"))
        ok &= _assert("/public/vendors/verify", "GET", r1, expected_status=200,
                       start=time.time())

        r1b = self.client.get(self._url("/public/vendors/verify?query=Pangan"))
        ok &= _assert("/public/vendors/verify", "GET", r1b, expected_status=200)

        # GET /public/dashboard/summary
        r2 = self.client.get(self._url("/public/dashboard/summary"))
        expected_keys = [
            "total_vendor_aktif", "total_vendor_termonitor_persen",
            "total_pengaduan_bulan_ini", "pengaduan_tertindaklanjuti_persen",
        ]
        ok &= _assert("/public/dashboard/summary", "GET", r2, expected_status=200,
                       check_json_keys=expected_keys)

        return ok

    # ── Admin ─────────────────────────────────────────────────────────────

    def test_admin(self) -> bool:
        if not self.token:
            for ep in ["/admin/users"]:
                report(ep, "POST/GET", "SKIP", detail="no token")
            return False
        ok = True

        # POST /admin/users
        unique = _new_uuid()[:8]
        user_payload = {
            "email": f"newuser-{unique}@test.com",
            "name": "New User",
            "password": "password123",
            "role": "vendor",
            "scope_value": ["DKI Jakarta"],
        }
        start = time.time()
        r1 = self.client.post(
            self._url("/admin/users"), json=user_payload,
            headers={**self.auth_headers, **_ik()},
        )
        ok &= _assert("/admin/users", "POST", r1, expected_status=201,
                       check_json_keys=["email", "role"], start=start)

        # POST /admin/users missing required → 422
        r1b = self.client.post(
            self._url("/admin/users"), json={"email": "incomplete@test.com"},
            headers={**self.auth_headers, **_ik()},
        )
        ok &= _assert("/admin/users", "POST", r1b, expected_status=422,
                       fail_detail="missing required fields")

        # POST /admin/users without auth → 401
        r1c = self.client.post(
            self._url("/admin/users"), json=user_payload, headers=_ik(),
        )
        ok &= _assert("/admin/users", "POST", r1c, expected_status=401,
                       fail_detail="no auth should 401")

        # GET /admin/users
        start = time.time()
        r2 = self.client.get(self._url("/admin/users"), headers=self.auth_headers)
        ok &= _assert("/admin/users", "GET", r2, expected_status=200, start=start)

        return ok

    # ── Audit logs ────────────────────────────────────────────────────────

    def test_audit_logs(self) -> bool:
        if not self.token:
            report("/audit-logs", "GET", "SKIP", detail="no token")
            return False
        ok = True

        start = time.time()
        r1 = self.client.get(self._url("/audit-logs"), headers=self.auth_headers)
        ok &= _assert("/audit-logs", "GET", r1, expected_status=200,
                       check_json_key="data", start=start)

        r1b = self.client.get(
            self._url("/audit-logs?entity_type=vendor&action=CREATE"),
            headers=self.auth_headers,
        )
        ok &= _assert("/audit-logs", "GET", r1b, expected_status=200)

        return ok

    # ── Runner ────────────────────────────────────────────────────────────

    def run_all(self) -> int:
        """Run all endpoint groups. Returns number of failures."""
        print(f"\n{'='*60}")
        print(f"  SIGAP API Contract Tester v0.2.0")
        print(f"  Target: {self.base}")
        print(f"{'='*60}\n")

        # 1. Auth
        print("\n── Auth ──")
        if self._should_run(["auth"]):
            self.test_auth_login()
            self.test_auth_me()
            self.test_auth_permissions()
        else:
            for ep in ["/auth/login", "/auth/me", "/auth/me/permissions"]:
                report(ep, "POST/GET", "SKIP", detail="tag filter")

        # 2. Vendor
        print("\n── Vendor ──")
        vendor_id: str | None = None
        if self._should_run(["vendor"]):
            self.test_vendor_crud()
            # Grab vendor ID from last created vendor
            if self.token:
                r = self.client.get(self._url("/vendors"), headers=self.auth_headers)
                if r.status_code == 200:
                    data = r.json().get("data", [])
                    if data:
                        vendor_id = data[0].get("id")
        else:
            for ep in ["/vendors", "/vendors/{id}"]:
                report(ep, "POST/GET", "SKIP", detail="tag filter")

        # 3. Distribution
        print("\n── Distribution ──")
        if self._should_run(["distribution"]):
            self.test_distributions(vendor_id)
        else:
            for ep in ["/distributions"]:
                report(ep, "POST/GET", "SKIP", detail="tag filter")

        # 4. Complaint
        print("\n── Complaint ──")
        if self._should_run(["complaint"]):
            self.test_complaints(vendor_id)
        else:
            for ep in ["/complaints"]:
                report(ep, "POST/GET", "SKIP", detail="tag filter")

        # 5. Public
        print("\n── Public ──")
        if self._should_run(["public"]):
            self.test_public()
        else:
            for ep in ["/public/vendors/verify", "/public/dashboard/summary"]:
                report(ep, "GET", "SKIP", detail="tag filter")

        # 6. Admin
        print("\n── Admin ──")
        if self._should_run(["admin"]):
            self.test_admin()
        else:
            for ep in ["/admin/users"]:
                report(ep, "POST/GET", "SKIP", detail="tag filter")

        # 7. Audit logs
        print("\n── Audit Logs ──")
        if self._should_run(["admin"]):
            self.test_audit_logs()
        else:
            report("/audit-logs", "GET", "SKIP", detail="tag filter")

        # Summary
        print_summary()
        return _fail_count


# ── CLI ─────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="SIGAP API Contract Tester v0.2.0")
    parser.add_argument("--base-url", default=BASE_URL,
                        help=f"Base URL (default: {BASE_URL})")
    parser.add_argument("--email", default=VALID_LOGIN["username"],
                        help="Login email")
    parser.add_argument("--password", default=VALID_LOGIN["password"],
                        help="Login password")
    parser.add_argument("--tags", default="",
                        help="Comma-separated tag filter (Auth,Vendor,Distribution,Complaint,Public,Admin)")
    parser.add_argument("--report", default="",
                        help="Save JSON report to file")
    args = parser.parse_args()

    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else None

    tester = ContractTester(args.base_url, args.email, args.password, tags)
    failures = tester.run_all()

    if args.report:
        save_report(args.report)

    tester.client.close()
    return 1 if failures > 0 else 0


if __name__ == "__main__":
    sys.exit(main())