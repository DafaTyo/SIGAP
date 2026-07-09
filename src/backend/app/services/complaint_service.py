from datetime import date, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.complaint import Complaint


def _normalize_date(value):
    if value is None:
        return None
    if isinstance(value, date):
        return value
    return datetime.strptime(str(value), "%Y-%m-%d").date()


def create_complaint(
    db: Session,
    *,
    vendor_id: str,
    kategori: str,
    deskripsi: str,
    distribution_id: str | None = None,
    nama_pelapor: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    foto_url: str | None = None,
    tanggal_kejadian: str | date | None = None,
    severity: str = "rendah",
    status: str = "baru",
) -> Complaint:
    complaint = Complaint(
        ticket_number=f"SG-{datetime.utcnow():%Y%m%d}-{uuid4().hex[:6].upper()}",
        vendor_id=vendor_id,
        distribution_id=distribution_id,
        nama_pelapor=nama_pelapor,
        kategori=kategori,
        deskripsi=deskripsi,
        latitude=latitude,
        longitude=longitude,
        foto_url=foto_url,
        tanggal_kejadian=_normalize_date(tanggal_kejadian),
        severity=severity,
        status=status,
        created_at=datetime.utcnow(),
    )
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint
