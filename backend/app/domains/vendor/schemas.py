
from datetime import datetime
from uuid import UUID
from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')

class Pagination(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int

class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    pagination: Pagination

class VendorCreate(BaseModel):
    nama_usaha: str
    nik_penanggung_jawab: str = Field(..., min_length=16, max_length=16)
    nib: str
    alamat: str
    provinsi: str
    kabupaten_kota: str
    kontak_telepon: Optional[str] = None

class VendorUpdate(BaseModel):
    alamat: Optional[str] = None
    kontak_telepon: Optional[str] = None

class VendorVerifyRequest(BaseModel):
    decision: str = Field(..., pattern="^(approve|reject)$")
    notes: Optional[str] = None

class VendorNikReveal(BaseModel):
    vendor_id: UUID
    nik_penanggung_jawab: str
    revealed_by: UUID
    revealed_at: datetime


class VendorDocument(BaseModel):
    id: UUID
    vendor_id: UUID
    document_type: str
    file_url: str
    validation_status: str
    validated_via: str | None = None


class DocumentValidationStatus(BaseModel):
    status: str
    validated_via: str | None
    validated_at: datetime


class SIODigitalRead(BaseModel):
    vendor_id: UUID
    sio_code: str
    qr_code_url: str
    issued_at: datetime
    valid_until: datetime


class VendorScoreRead(BaseModel):
    vendor_id: UUID
    score: float
    factors: dict
    last_updated: datetime


class PublicVendorProfile(BaseModel):
    nama_usaha: str
    kabupaten_kota: str
    provinsi: str
    status: str
    sio_code: str | None = None
    valid_until: datetime | None = None


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
