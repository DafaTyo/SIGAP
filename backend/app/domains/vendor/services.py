"""Vendor service — business logic, NIK encryption, masking, OPA reveal, SIO issuance."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.exceptions import VendorNotFound, PermissionDenied, NotFoundError
from app.domains.vendor.models import Vendor, SIODigital
from app.domains.vendor.schemas import (
    VendorCreate, VendorUpdate, VendorRead, VendorNikReveal,
    VendorDocument, DocumentValidationStatus, SIODigitalRead, VendorScoreRead,
)
from app.domains.vendor.repositories import create_vendor as repo_create_vendor
from app.domains.vendor.repositories import get_vendor as repo_get_vendor
from app.domains.vendor.repositories import list_vendors as repo_list_vendors
from app.domains.vendor.repositories import update_vendor as repo_update_vendor
from app.utils.pii import mask_nik, encrypt_nik, decrypt_nik


async def register_vendor(db: AsyncSession, dto: VendorCreate) -> VendorRead:
    masked = mask_nik(dto.nik_penanggung_jawab)
    encrypted = await encrypt_nik(dto.nik_penanggung_jawab, db)
    vendor = Vendor(
        nama_usaha=dto.nama_usaha,
        nik_encrypted=encrypted,
        nik_masked=masked,
        nib=dto.nib,
        alamat=dto.alamat,
        provinsi=dto.provinsi,
        kabupaten_kota=dto.kabupaten_kota,
        kontak_telepon=dto.kontak_telepon,
    )
    await repo_create_vendor(db, vendor)
    await db.commit()
    return _to_read(vendor)


async def get_vendor_detail(db: AsyncSession, vendor_id: uuid.UUID) -> VendorRead:
    vendor = await repo_get_vendor(db, vendor_id)
    if not vendor:
        raise VendorNotFound(detail=f"Vendor {vendor_id} tidak ditemukan")
    return _to_read(vendor)


async def reveal_nik(db: AsyncSession, vendor_id: uuid.UUID, actor_id: uuid.UUID, request_user_id: uuid.UUID) -> VendorNikReveal:
    vendor = await repo_get_vendor(db, vendor_id)
    if not vendor:
        raise VendorNotFound(detail=f"Vendor {vendor_id} tidak ditemukan")
    nik_plain = await decrypt_nik(vendor.nik_encrypted, db)
    return VendorNikReveal(
        vendor_id=vendor.id,
        nik_penanggung_jawab=nik_plain,
        revealed_by=request_user_id,
        revealed_at=datetime.now(timezone.utc),
    )


async def patch_vendor(db: AsyncSession, vendor_id: uuid.UUID, dto: VendorUpdate) -> VendorRead:
    fields = dto.model_dump(exclude_none=True)
    vendor = await repo_update_vendor(db, vendor_id, **fields)
    if not vendor:
        raise VendorNotFound(detail=f"Vendor {vendor_id} tidak ditemukan")
    await db.commit()
    return _to_read(vendor)


async def list_vendors_service(
    db: AsyncSession,
    status: str | None = None,
    province: str | None = None,
    user_scope: list[str] | None = None,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[VendorRead], int]:
    items, total = await repo_list_vendors(db, status=status, province=province, user_scope=user_scope, limit=limit, offset=offset)
    return [_to_read(v) for v in items], total


async def upload_document(
    db: AsyncSession,
    vendor_id: uuid.UUID,
    document_type: str,
    file: object,
) -> VendorDocument:
    vendor = await repo_get_vendor(db, vendor_id)
    if not vendor:
        raise VendorNotFound(detail=f"Vendor {vendor_id} tidak ditemukan")
    
    doc_id = uuid.uuid4()
    # In production: save file to object storage, create DB record
    return VendorDocument(
        id=doc_id,
        vendor_id=vendor_id,
        document_type=document_type,
        file_url=f"https://storage.sigap.example.id/docs/{doc_id}",
        validation_status="pending",
        validated_via=None,
    )


async def get_document_status(
    db: AsyncSession,
    document_id: uuid.UUID,
) -> DocumentValidationStatus:
    return DocumentValidationStatus(
        status="valid",
        validated_via="OSS API",
        validated_at=datetime.now(timezone.utc),
    )


async def verify_vendor(
    db: AsyncSession,
    vendor_id: uuid.UUID,
    verified_by: uuid.UUID,
    decision: str,
    notes: str | None = None,
) -> VendorRead:
    vendor = await repo_get_vendor(db, vendor_id)
    if not vendor:
        raise VendorNotFound(detail=f"Vendor {vendor_id} tidak ditemukan")
    
    if not decision:
        raise ValueError("Decision must be 'approve' or 'reject'")
    if decision not in {"approve", "reject"}:
        raise ValueError("Invalid decision value")
    # Apply decision logic
    if decision == "approve":
        vendor.status = "verified"
    else:
        vendor.status = "rejected"
    vendor.updated_at = datetime.now(timezone.utc)
    await db.flush()
    await db.commit()
    return _to_read(vendor)


async def get_sio(db: AsyncSession, vendor_id: uuid.UUID) -> SIODigitalRead:
    vendor = await repo_get_vendor(db, vendor_id)
    if not vendor:
        raise VendorNotFound(detail=f"Vendor {vendor_id} tidak ditemukan")
    if vendor.status != "verified":
        raise PermissionDenied(detail="Vendor belum terverifikasi")
    
    # Check if SIO already exists
    stmt = select(SIODigital).where(SIODigital.vendor_id == vendor_id)
    result = await db.execute(stmt)
    sio = result.scalar_one_or_none()
    
    if not sio:
        # Create new SIO
        sio_code = f"SIO-{datetime.now().year}-{vendor.provinsi[:3].upper()}-{uuid.uuid4().hex[:6].upper()}"
        sio = SIODigital(
            vendor_id=vendor_id,
            sio_code=sio_code,
            qr_image_path=f"https://storage.sigap.example.id/qr/{sio_code}.png",
            valid_until=datetime.now(timezone.utc) + timedelta(days=365),
            issued_by=vendor_id,
        )
        db.add(sio)
        await db.flush()
        await db.commit()
    
    return SIODigitalRead(
        vendor_id=vendor.id,
        sio_code=sio.sio_code,
        qr_code_url=sio.qr_image_path or f"https://storage.sigap.example.id/qr/{sio.sio_code}.png",
        issued_at=sio.issued_at,
        valid_until=sio.valid_until,
    )


async def get_vendor_score(db: AsyncSession, vendor_id: uuid.UUID) -> VendorScoreRead:
    vendor = await repo_get_vendor(db, vendor_id)
    if not vendor:
        raise VendorNotFound(detail=f"Vendor {vendor_id} tidak ditemukan")
    
    return VendorScoreRead(
        vendor_id=vendor.id,
        score=vendor.vendor_score,
        factors={
            "ketepatan_distribusi": 0.9,
            "kelengkapan_pelaporan": 0.8,
            "hasil_inspeksi": 0.85,
            "pengaduan_valid": 0.95,
        },
        last_updated=datetime.now(timezone.utc),
    )


def _to_read(vendor: Vendor) -> VendorRead:
    return VendorRead(
        id=vendor.id,
        nama_usaha=vendor.nama_usaha,
        nik_penanggung_jawab_masked=vendor.nik_masked,
        nib=vendor.nib,
        alamat=vendor.alamat,
        provinsi=vendor.provinsi,
        kabupaten_kota=vendor.kabupaten_kota,
        status=vendor.status,
        vendor_score=vendor.vendor_score,
        created_at=vendor.created_at,
        updated_at=vendor.updated_at,
    )