"""Tests for vendor endpoints with async client."""

from __future__ import annotations

import pytest


@pytest.mark.anyio
class TestVendors:
    async def test_health_check(self, client):
        resp = await client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}

    async def test_create_vendor(self, client, auth_headers):
        payload = {
            "nama_usaha": "Warung Berkah",
            "nik_penanggung_jawab": "1234567890123456",
            "nib": "NIB-888292",
            "alamat": "Jl. Merdeka No. 10",
            "provinsi": "DKI Jakarta",
            "kabupaten_kota": "Jakarta Pusat",
        }
        resp = await client.post("/v1/vendors", json=payload, headers=auth_headers)
        assert resp.status_code == 201
        data = resp.json()
        assert data["nama_usaha"] == "Warung Berkah"
        assert data["nik_penanggung_jawab_masked"] == "1234********3456"
        assert "id" in data

    async def test_create_vendor_invalid_nik(self, client, auth_headers):
        payload = {
            "nama_usaha": "Test",
            "nik_penanggung_jawab": "123",  # too short
            "nib": "NIB-000",
            "alamat": "Jl. Test",
            "provinsi": "DKI Jakarta",
            "kabupaten_kota": "Jakarta Pusat",
        }
        resp = await client.post("/v1/vendors", json=payload, headers=auth_headers)
        assert resp.status_code == 422

    async def test_list_vendors_paginated(self, client, auth_headers):
        resp = await client.get("/v1/vendors?page=1&page_size=10", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "data" in data
        assert "pagination" in data
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["page_size"] == 10

    async def test_get_nonexistent_vendor(self, client, auth_headers):
        resp = await client.get("/v1/vendors/00000000-0000-0000-0000-000000000000", headers=auth_headers)
        assert resp.status_code == 404
