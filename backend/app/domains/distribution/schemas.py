"""Distribution schemas — 1:1 with api-contract.yaml."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DistributionCreate(BaseModel):
    vendor_id: UUID
    jumlah_porsi: int
    lokasi_sekolah: str | None = None
    latitude: float
    longitude: float


class DistributionRead(BaseModel):
    id: UUID
    vendor_id: UUID
    jumlah_porsi: int
    lokasi_sekolah: str | None
    latitude: float
    longitude: float
    foto_url: str | None
    reported_at: datetime
    photo_taken_at: datetime | None
    tampering_suspicion: bool
