"""Complaint service — ticket generation, SLA, severity mapping."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.domains.complaint.models import Complaint
from app.domains.complaint.schemas import ComplaintCreate, ComplaintRead, ComplaintUpdate
from app.domains.complaint.repositories import (
    create_complaint as repo_create_complaint,
    get_complaint as repo_get_complaint,
    list_complaints as repo_list_complaints,
    update_complaint as repo_update_complaint,
)


async def submit_complaint(db: AsyncSession, dto: ComplaintCreate) -> ComplaintRead:
    ticket = f"SG-{datetime.now(timezone.utc).year}-{uuid.uuid4().hex[:6].upper()}"
    # Naive severity mapping
    severity = "kritis" if dto.kategori == "keracunan" else "sedang"
    complaint = Complaint(
        vendor_id=dto.vendor_id,
        ticket_number=ticket,
        nama_pelapor=dto.nama_pelapor,
        kategori=dto.kategori,
        deskripsi=dto.deskripsi,
        severity=severity,
    )
    await repo_create_complaint(db, complaint)
    await db.commit()
    return _to_read(complaint)


async def get_detail(db: AsyncSession, complaint_id: uuid.UUID) -> ComplaintRead:
    complaint = await repo_get_complaint(db, complaint_id)
    if not complaint:
        raise NotFoundError(detail=f"Complaint {complaint_id} tidak ditemukan")
    return _to_read(complaint)


async def patch_complaint(
    db: AsyncSession,
    complaint_id: uuid.UUID,
    dto: ComplaintUpdate,
) -> ComplaintRead:
    fields = dto.model_dump(exclude_none=True)
    complaint = await repo_update_complaint(db, complaint_id, **fields)
    if not complaint:
        raise NotFoundError(detail=f"Complaint {complaint_id} tidak ditemukan")
    await db.commit()
    return _to_read(complaint)


async def list_complaints(
    db: AsyncSession,
    status: str | None = None,
    severity: str | None = None,
    user_scope: list[str] | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[ComplaintRead], int]:
    items, total = await repo_list_complaints(db, status=status, severity=severity, user_scope=user_scope, limit=limit, offset=offset)
    return [_to_read(c) for c in items], total


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
        photo_url=getattr(c, 'photo_url', None),
        latitude=getattr(c, 'latitude', None),
        longitude=getattr(c, 'longitude', None),
        province=getattr(c, 'province', None),
        nama_pelapor=c.nama_pelapor,
        created_at=c.created_at,
        updated_at=getattr(c, 'updated_at', None),
        sla_deadline=c.sla_deadline,
    )