from sqlalchemy.orm import Session

from app.models.vendor import Vendor
from app.services.audit_log_service import create_audit_log


def create_vendor(
    db: Session,
    *,
    nama_usaha: str,
    nik_penanggung_jawab: str,
    nib: str,
    alamat: str,
    provinsi: str,
    kabupaten_kota: str,
    kontak_telepon: str | None = None,
) -> Vendor:
    vendor = Vendor(
        nama_usaha=nama_usaha,
        nik_penanggung_jawab=nik_penanggung_jawab,
        nib=nib,
        alamat=alamat,
        provinsi=provinsi,
        kabupaten_kota=kabupaten_kota,
        kontak_telepon=kontak_telepon,
    )
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor


def get_vendor(db: Session, vendor_id: str) -> Vendor | None:
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()


def update_vendor(
    db: Session,
    *,
    vendor_id: str,
    actor_id: str | None = None,
    **changes,
) -> Vendor:
    vendor = get_vendor(db, vendor_id)
    if vendor is None:
        raise ValueError("Vendor tidak ditemukan")

    old_values = {key: getattr(vendor, key) for key in changes.keys() if hasattr(vendor, key)}
    for key, value in changes.items():
        if hasattr(vendor, key):
            setattr(vendor, key, value)

    db.add(vendor)
    db.commit()
    db.refresh(vendor)

    create_audit_log(
        db,
        entity_type="vendor",
        entity_id=vendor.id,
        action="UPDATE",
        actor_id=actor_id,
        old_values=old_values,
        new_values={key: getattr(vendor, key) for key in old_values.keys()},
    )
    return vendor
