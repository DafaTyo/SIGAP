"""Vendor repository — CRUD operations with scope filtering and pagination."""

from __future__ import annotations

import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.vendor.models import Vendor


async def create_vendor(db: AsyncSession, vendor: Vendor) -> Vendor:
    db.add(vendor)
    await db.flush()
    return vendor


async def get_vendor(db: AsyncSession, vendor_id: uuid.UUID) -> Vendor | None:
    return await db.get(Vendor, vendor_id)


async def list_vendors(
    db: AsyncSession,
    status: str | None = None,
    province: str | None = None,
    user_scope: list[str] | None = None,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[Vendor], int]:
    # Count total first
    count_q = select(func.count()).select_from(Vendor)
    if status:
        count_q = count_q.where(Vendor.status == status)
    if province:
        count_q = count_q.where(Vendor.provinsi == province)
    if user_scope:
        count_q = count_q.where(Vendor.provinsi.in_(user_scope))
    total = await db.scalar(count_q) or 0

    # Fetch page
    stmt = select(Vendor).limit(limit).offset(offset)
    if status:
        stmt = stmt.where(Vendor.status == status)
    if province:
        stmt = stmt.where(Vendor.provinsi == province)
    if user_scope:
        stmt = stmt.where(Vendor.provinsi.in_(user_scope))
    stmt = stmt.order_by(Vendor.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all()), total


async def update_vendor(db: AsyncSession, vendor_id: uuid.UUID, **fields) -> Vendor | None:
    vendor = await db.get(Vendor, vendor_id)
    if vendor:
        for k, v in fields.items():
            setattr(vendor, k, v)
        await db.flush()
    return vendor
