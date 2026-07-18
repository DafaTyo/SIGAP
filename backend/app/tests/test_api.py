"""API endpoints integration tests for Layer 3."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_vendor_endpoint():
    payload = {
        "nama_usaha": "Warung Berkah",
        "nik_penanggung_jawab": "1234567890123456",
        "nib": "NIB-888292",
        "alamat": "Jl. Merdeka No. 10",
        "provinsi": "DKI Jakarta",
        "kabupaten_kota": "Jakarta Pusat",
    }
    response = client.post("/v1/vendors", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nama_usaha"] == "Warung Berkah"
    assert data["nik_penanggung_jawab_masked"] == "1234********3456"
    assert "id" in data


def test_list_vendors_endpoint():
    response = client.get("/v1/vendors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_distribution_endpoint():
    # First create a vendor to get vendor_id
    payload_vendor = {
        "nama_usaha": "Catering Sehat",
        "nik_penanggung_jawab": "9876543210987654",
        "nib": "NIB-11111",
        "alamat": "Jl. Sudirman",
        "provinsi": "Jawa Barat",
        "kabupaten_kota": "Bandung",
    }
    v_resp = client.post("/v1/vendors", json=payload_vendor)
    vendor_id = v_resp.json()["id"]

    payload_dist = {
        "vendor_id": vendor_id,
        "jumlah_porsi": 150,
        "lokasi_sekolah": "SDN 01 Bandung",
        "latitude": -6.914744,
        "longitude": 107.609810,
    }
    response = client.post("/v1/distributions", json=payload_dist)
    assert response.status_code == 201
    data = response.json()
    assert data["jumlah_porsi"] == 150
    assert data["tampering_suspicion"] is False


def test_create_complaint_endpoint():
    payload_vendor = {
        "nama_usaha": "Dapur Kita",
        "nik_penanggung_jawab": "1122334455667788",
        "nib": "NIB-22222",
        "alamat": "Jl. Thamrin",
        "provinsi": "DKI Jakarta",
        "kabupaten_kota": "Jakarta Pusat",
    }
    v_resp = client.post("/v1/vendors", json=payload_vendor)
    vendor_id = v_resp.json()["id"]

    payload_complaint = {
        "vendor_id": vendor_id,
        "kategori": "keterlambatan",
        "deskripsi": "Makanan terlambat datang 1 jam",
    }
    response = client.post("/v1/complaints", json=payload_complaint)
    assert response.status_code == 201
    data = response.json()
    assert data["kategori"] == "keterlambatan"
    assert "ticket_number" in data
