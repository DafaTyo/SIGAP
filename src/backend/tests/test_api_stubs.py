import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "sigap-backend"}

def test_public_dashboard_summary():
    response = client.get("/v1/public/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_vendor_aktif" in data
    assert "total_pengaduan_bulan_ini" in data

def test_auth_me_permissions():
    response = client.get("/v1/auth/me/permissions")
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "pengawas_dinas"
    assert "scope" in data
    assert type(data["scope"]["value"]) == list

def test_missing_route_returns_404():
    response = client.get("/v1/not-found-route")
    assert response.status_code == 404

def test_create_vendor_idempotency():
    headers = {"X-Idempotency-Key": "test-key-123"}
    response = client.post("/v1/vendors", headers=headers)
    # The current stub returns 200
    assert response.status_code == 200
    data = response.json()
    assert data["idempotency_key"] == "test-key-123"

def test_get_sio_digital():
    response = client.get("/v1/vendors/test-vendor-uuid/sio")
    assert response.status_code == 200
    assert response.json()["vendor_id"] == "test-vendor-uuid"
