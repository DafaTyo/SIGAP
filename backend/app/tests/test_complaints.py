"""Tests for complaint endpoints."""

from __future__ import annotations

import pytest


@pytest.mark.anyio
class TestComplaints:
    async def test_submit_complaint(self, client, auth_headers):
        # First create a vendor
        v_resp = await client.post("/v1/vendors", json={
            "nama_usaha": "Dapur Kita",
            "nik_penanggung_jawab": "1122334455667788",
            "nib": "NIB-22222",
            "alamat": "Jl. Thamrin",
            "provinsi": "DKI Jakarta",
            "kabupaten_kota": "Jakarta Pusat",
        }, headers=auth_headers)
        vendor_id = v_resp.json()["id"]

        payload = {
            "vendor_id": vendor_id,
            "kategori": "keterlambatan",
            "deskripsi": "Makanan terlambat datang 1 jam",
        }
        resp = await client.post("/v1/complaints", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert "ticket_number" in data
        assert data["kategori"] == "keterlambatan"

    async def test_list_complaints_paginated(self, client, auth_headers):
        resp = await client.get("/v1/complaints?page=1&page_size=10", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "data" in data
        assert "pagination" in data
