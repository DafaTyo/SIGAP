"""Complaint repository."""

from __future__ import annotations

import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.complaint.models import Complaint


async def create_complaint(db: AsyncSession, complaint: Complaint) -> Complaint:
    db.add(complaint)
    await db.flush()
    return complaint


async def get_complaint(db: AsyncSession, complaint_id: uuid.UUID) -> Complaint | None:
    return await db.get(Complaint, complaint_id)


async def list_complaints(db: AsyncSession, status: str | None = None) -> list[Complaint]:
    stmt = select(Complaint)
    if status:
        stmt = stmt.where(Complaint.status == status)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def update_complaint(db: AsyncSession, complaint_id: uuid.UUID, **fields) -> Complaint | None:
    complaint = await db.get(Complaint, complaint_id)
    if complaint:
        for k, v in fields.items():
            setattr(complaint, k, v)
        await db.flush()
    return complaint
