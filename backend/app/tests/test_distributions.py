"""Tests for distribution endpoints."""

from __future__ import annotations

import pytest


@pytest.mark.anyio
class TestDistributions:
    async def test_submit_distribution(self, client, auth_headers):
        v_resp = await client.post("/v1/vendors", json={
            "nama_usaha": "Catering Sehat",
            "nik_penanggung_jawab": "9876543210987654",
            "nib": "NIB-11111",
            "alamat": "Jl. Sudirman",
            "provinsi": "Jawa Barat",
            "kabupaten_kota": "Bandung",
        }, headers=auth_headers)
        vendor_id = v_resp.json()["id"]

        payload = {
            "vendor_id": vendor_id,
            "jumlah_porsi": 150,
            "lokasi_sekolah": "SDN 01 Bandung",
            "latitude": -6.914744,
            "longitude": 107.609810,
        }
        resp = await client.post("/v1/distributions", json=payload, headers=auth_headers)
        assert resp.status_code == 201
        data = resp.json()
        assert data["jumlah_porsi"] == 150

    async def test_list_distributions_paginated(self, client, auth_headers):
        resp = await client.get("/v1/distributions?page=1&page_size=10", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "data" in data
        assert "pagination" in data
