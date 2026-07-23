from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GeoValidation(BaseModel):
    is_within_radius: bool
    distance_meters: float
    school_name: str


class DistributionCreate(BaseModel):
    vendor_id: UUID
    jumlah_porsi: int
    lokasi_sekolah: str | None = None
    latitude: float
    longitude: float
    metadata: dict | None = None  # expects capture_time etc.


class DistributionRead(BaseModel):
    id: UUID
    vendor_id: UUID
    jumlah_porsi: int
    lokasi_sekolah: str | None
    latitude: float
    longitude: float
    foto_url: str | None = None
    reported_at: datetime
    photo_taken_at: datetime | None = None
    tampering_suspicion: bool
    geo_validation: GeoValidation | None = None
    anomaly: dict | None = None


class DistributionMetadata(BaseModel):
    distribution_id: UUID
    photo_taken_at: datetime | None = None
    exif_timestamp: datetime | None = None
    device_id: str | None = None
    latitude: float
    longitude: float
    tampering_suspicion: bool
    created_at: datetime


class AppealResponse(BaseModel):
    distribution_id: UUID
    appeal_status: str
    is_frozen: bool = True
    submitted_at: datetime
