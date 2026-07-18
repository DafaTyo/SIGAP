"""Complaint schemas — 1:1 with api-contract.yaml."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ComplaintCreate(BaseModel):
    vendor_id: UUID
    nama_pelapor: str | None = None
    kategori: str
    deskripsi: str
    latitude: float | None = None
    longitude: float | None = None
    distribution_id: UUID | None = None
    tanggal_kejadian: str | None = None


class ComplaintRead(BaseModel):
    id: UUID
    ticket_number: str
    vendor_id: UUID
    kategori: str
    deskripsi: str
    severity: str
    status: str
    resolution_notes: str | None
    created_at: datetime
    sla_deadline: datetime


class ComplaintUpdate(BaseModel):
    status: str | None = None
    resolution_notes: str | None = None
