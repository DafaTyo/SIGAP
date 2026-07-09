import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.services.audit_log_service import create_audit_log
from app.services.complaint_service import create_complaint
from app.services.distribution_service import create_distribution_report
from app.services.vendor_service import create_vendor, update_vendor


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_vendor_persists_vendor(db_session):
    vendor = create_vendor(
        db_session,
        nama_usaha="SPPG Contoh",
        nik_penanggung_jawab="3175123412345678",
        nib="1234567890123",
        alamat="Jl. Contoh",
        provinsi="DKI Jakarta",
        kabupaten_kota="Jakarta Pusat",
        kontak_telepon="08123456789",
    )

    assert vendor.id
    assert vendor.status == "pending_verification"
    assert vendor.nama_usaha == "SPPG Contoh"


def test_update_vendor_writes_audit_log(db_session):
    vendor = create_vendor(
        db_session,
        nama_usaha="SPPG Lama",
        nik_penanggung_jawab="3175123412345678",
        nib="1234567890123",
        alamat="Jl. Lama",
        provinsi="DKI Jakarta",
        kabupaten_kota="Jakarta Pusat",
    )

    updated = update_vendor(
        db_session,
        vendor_id=vendor.id,
        actor_id="admin-1",
        alamat="Jl. Baru",
        kontak_telepon="0899999999",
    )

    assert updated.alamat == "Jl. Baru"
    audit_logs = db_session.query(Base.metadata.tables["audit_logs"]).all()
    assert len(audit_logs) == 1


def test_create_distribution_report_persists_radius_and_anomaly(db_session):
    vendor = create_vendor(
        db_session,
        nama_usaha="SPPG Distribusi",
        nik_penanggung_jawab="3175123412345678",
        nib="9999999999999",
        alamat="Jl. Distribusi",
        provinsi="DKI Jakarta",
        kabupaten_kota="Jakarta Pusat",
    )

    report = create_distribution_report(
        db_session,
        vendor_id=vendor.id,
        jumlah_porsi=500,
        lokasi_sekolah="SD Contoh",
        latitude=-6.2,
        longitude=106.8,
        radius=250.0,
        anomaly={"score": 0.12, "flag": "none", "detected": False},
    )

    assert report.id
    assert report.radius == 250.0
    assert report.anomaly["detected"] is False


def test_create_complaint_can_link_to_distribution(db_session):
    vendor = create_vendor(
        db_session,
        nama_usaha="SPPG Aduan",
        nik_penanggung_jawab="3175123412345678",
        nib="8888888888888",
        alamat="Jl. Aduan",
        provinsi="DKI Jakarta",
        kabupaten_kota="Jakarta Pusat",
    )
    report = create_distribution_report(
        db_session,
        vendor_id=vendor.id,
        jumlah_porsi=500,
        lokasi_sekolah="SD Contoh",
        latitude=-6.2,
        longitude=106.8,
    )

    complaint = create_complaint(
        db_session,
        vendor_id=vendor.id,
        distribution_id=report.id,
        kategori="kualitas_makanan",
        deskripsi="Makanan basi",
        tanggal_kejadian="2026-07-09",
    )

    assert complaint.ticket_number.startswith("SG-")
    assert complaint.distribution_id == report.id


def test_create_audit_log_persists_change_payload(db_session):
    log = create_audit_log(
        db_session,
        entity_type="vendor",
        entity_id="vendor-1",
        action="UPDATE",
        actor_id="admin-1",
        old_values={"alamat": "A"},
        new_values={"alamat": "B"},
        ip_address="127.0.0.1",
    )

    assert log.id
    assert log.action == "UPDATE"
    assert log.old_values == {"alamat": "A"}
