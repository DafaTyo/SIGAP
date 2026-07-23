"""Complaint repository — CRUD with pagination."""

from __future__ import annotations

import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.complaint.models import Complaint


async def create_complaint(db: AsyncSession, complaint: Complaint) -> Complaint:
    db.add(complaint)
    await db.flush()
    return complaint


async def get_complaint(db: AsyncSession, complaint_id: uuid.UUID) -> Complaint | None:
    return await db.get(Complaint, complaint_id)


async def list_complaints(
    db: AsyncSession,
    status: str | None = None,
    severity: str | None = None,
    user_scope: list[str] | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[Complaint], int]:
    # Count
    count_q = select(func.count()).select_from(Complaint)
    if status:
        count_q = count_q.where(Complaint.status == status)
    if severity:
        count_q = count_q.where(Complaint.severity == severity)
    if user_scope:
        count_q = count_q.where(Complaint.province.in_(user_scope))
    total = await db.scalar(count_q) or 0

    # Fetch
    stmt = select(Complaint).limit(limit).offset(offset)
    if status:
        stmt = stmt.where(Complaint.status == status)
    if severity:
        stmt = stmt.where(Complaint.severity == severity)
    if user_scope:
        stmt = stmt.where(Complaint.province.in_(user_scope))
    stmt = stmt.order_by(Complaint.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all()), total


async def update_complaint(db: AsyncSession, complaint_id: uuid.UUID, **fields) -> Complaint | None:
    complaint = await db.get(Complaint, complaint_id)
    if complaint:
        for k, v in fields.items():
            setattr(complaint, k, v)
        await db.flush()
    return complaint
