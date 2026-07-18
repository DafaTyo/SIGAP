"""Vendor service — business logic, NIK encryption, masking, OPA reveal."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import VendorNotFound, PermissionDenied
from app.domains.vendor.models import Vendor
from app.domains.vendor.schemas import VendorCreate, VendorUpdate, VendorRead, VendorNikReveal
from app.domains.vendor.repositories import create_vendor, get_vendor, list_vendors, update_vendor
from app.utils.pii import mask_nik


async def register_vendor(db: AsyncSession, dto: VendorCreate) -> VendorRead:
    masked = mask_nik(dto.nik_penanggung_jawab)
    # ponytail: encrypt_nik stub — replace with pgcrypto call when DB session wired
    encrypted = dto.nik_penanggung_jawab.encode()  # placeholder until pgcrypto integrated
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
    await create_vendor(db, vendor)
    return _to_read(vendor)


async def get_vendor_detail(db: AsyncSession, vendor_id: uuid.UUID) -> VendorRead:
    vendor = await get_vendor(db, vendor_id)
    if not vendor:
        raise VendorNotFound(detail=f"Vendor {vendor_id} tidak ditemukan")
    return _to_read(vendor)


async def reveal_nik(db: AsyncSession, vendor_id: uuid.UUID, actor_id: uuid.UUID) -> VendorNikReveal:
    vendor = await get_vendor(db, vendor_id)
    if not vendor:
        raise VendorNotFound(detail=f"Vendor {vendor_id} tidak ditemukan")
    # ponytail: decrypt via pgcrypto — stub returns encoded bytes decoded
    nik_plain = vendor.nik_encrypted.decode()
    return VendorNikReveal(
        vendor_id=vendor.id,
        nik_penanggung_jawab=nik_plain,
        revealed_by=actor_id,
        revealed_at=datetime.now(timezone.utc),
    )


async def patch_vendor(db: AsyncSession, vendor_id: uuid.UUID, dto: VendorUpdate) -> VendorRead:
    fields = dto.model_dump(exclude_none=True)
    vendor = await update_vendor(db, vendor_id, **fields)
    if not vendor:
        raise VendorNotFound(detail=f"Vendor {vendor_id} tidak ditemukan")
    return _to_read(vendor)


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
