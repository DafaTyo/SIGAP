"""Pydantic schemas for Vendor domain — 1:1 with api-contract.yaml."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class VendorCreate(BaseModel):
    nama_usaha: str
    nik_penanggung_jawab: str = Field(..., min_length=16, max_length=16)
    nib: str
    alamat: str
    provinsi: str
    kabupaten_kota: str
    kontak_telepon: str | None = None


class VendorUpdate(BaseModel):
    alamat: str | None = None
    kontak_telepon: str | None = None


class VendorRead(BaseModel):
    id: UUID
    nama_usaha: str
    nik_penanggung_jawab_masked: str
    nib: str
    alamat: str
    provinsi: str
    kabupaten_kota: str
    status: str
    vendor_score: float
    created_at: datetime
    updated_at: datetime


class VendorNikReveal(BaseModel):
    vendor_id: UUID
    nik_penanggung_jawab: str
    revealed_by: UUID
    revealed_at: datetime
