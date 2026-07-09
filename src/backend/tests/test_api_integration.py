import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_vendor_distribution_complaint_flow(client):
    vendor_response = client.post(
        "/v1/vendors",
        json={
            "nama_usaha": "SPPG Integration",
            "nik_penanggung_jawab": "3175123412345678",
            "nib": "1234567890123",
            "alamat": "Jl. Integration",
            "provinsi": "DKI Jakarta",
            "kabupaten_kota": "Jakarta Pusat",
            "kontak_telepon": "08123456789",
        },
        headers={"X-Idempotency-Key": "vendor-create-1"},
    )
    assert vendor_response.status_code == 201
    vendor = vendor_response.json()
    assert vendor["id"]
    assert vendor["nama_usaha"] == "SPPG Integration"
    assert vendor["nik_penanggung_jawab_masked"] == "3175********5678"

    vendor_id = vendor["id"]
    list_response = client.get("/v1/vendors")
    assert list_response.status_code == 200
    assert len(list_response.json()["data"]) == 1

    update_response = client.patch(
        f"/v1/vendors/{vendor_id}",
        json={"alamat": "Jl. Updated", "kontak_telepon": "0899999999"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["alamat"] == "Jl. Updated"

    distribution_response = client.post(
        "/v1/distributions",
        json={
            "vendor_id": vendor_id,
            "jumlah_porsi": 500,
            "lokasi_sekolah": "SD Integration",
            "latitude": -6.2,
            "longitude": 106.8,
            "radius": 250,
            "anomaly": {"score": 0.1, "flag": "none", "detected": False},
        },
        headers={"X-Idempotency-Key": "distribution-create-1"},
    )
    assert distribution_response.status_code == 201
    distribution = distribution_response.json()
    assert distribution["radius"] == 250
    assert distribution["anomaly"]["detected"] is False

    complaint_response = client.post(
        "/v1/complaints",
        json={
            "vendor_id": vendor_id,
            "distribution_id": distribution["id"],
            "kategori": "kualitas_makanan",
            "deskripsi": "Makanan tidak layak",
            "tanggal_kejadian": "2026-07-09",
        },
        headers={"X-Idempotency-Key": "complaint-create-1"},
    )
    assert complaint_response.status_code == 201
    complaint = complaint_response.json()
    assert complaint["ticket_number"].startswith("SG-")
    assert complaint["distribution_id"] == distribution["id"]

    audit_response = client.get("/v1/audit-logs")
    assert audit_response.status_code == 200
    assert len(audit_response.json()["data"]) >= 1
