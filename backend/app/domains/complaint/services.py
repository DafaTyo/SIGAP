"""Complaint service — ticket generation, SLA, severity mapping."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.domains.complaint.models import Complaint
from app.domains.complaint.schemas import ComplaintCreate, ComplaintRead, ComplaintUpdate
from app.domains.complaint.repositories import create_complaint, get_complaint, list_complaints, update_complaint


async def submit_complaint(db: AsyncSession, dto: ComplaintCreate) -> ComplaintRead:
    ticket = f"SG-{datetime.now(timezone.utc).year}-{uuid.uuid4().hex[:6].upper()}"
    # ponytail: naive severity mapping — replace with ML/rules when available
    severity = "kritis" if dto.kategori == "keracunan" else "sedang"
    complaint = Complaint(
        vendor_id=dto.vendor_id,
        ticket_number=ticket,
        nama_pelapor=dto.nama_pelapor,
        kategori=dto.kategori,
        deskripsi=dto.deskripsi,
        severity=severity,
    )
    await create_complaint(db, complaint)
    return _to_read(complaint)


async def get_detail(db: AsyncSession, complaint_id: uuid.UUID) -> ComplaintRead:
    complaint = await get_complaint(db, complaint_id)
    if not complaint:
        raise NotFoundError(detail=f"Complaint {complaint_id} tidak ditemukan")
    return _to_read(complaint)


async def patch_complaint(db: AsyncSession, complaint_id: uuid.UUID, dto: ComplaintUpdate) -> ComplaintRead:
    fields = dto.model_dump(exclude_none=True)
    complaint = await update_complaint(db, complaint_id, **fields)
    if not complaint:
        raise NotFoundError(detail=f"Complaint {complaint_id} tidak ditemukan")
    return _to_read(complaint)


def _to_read(c: Complaint) -> ComplaintRead:
    return ComplaintRead(
        id=c.id,
        ticket_number=c.ticket_number,
        vendor_id=c.vendor_id,
        kategori=c.kategori,
        deskripsi=c.deskripsi,
        severity=c.severity,
        status=c.status,
        resolution_notes=c.resolution_notes,
        created_at=c.created_at,
        sla_deadline=c.sla_deadline,
    )
