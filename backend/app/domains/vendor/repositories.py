"""Vendor repository — CRUD operations."""

from __future__ import annotations

import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.vendor.models import Vendor


async def create_vendor(db: AsyncSession, vendor: Vendor) -> Vendor:
    db.add(vendor)
    await db.flush()
    return vendor


async def get_vendor(db: AsyncSession, vendor_id: uuid.UUID) -> Vendor | None:
    return await db.get(Vendor, vendor_id)


async def list_vendors(db: AsyncSession, status: str | None = None, province: str | None = None) -> list[Vendor]:
    stmt = select(Vendor)
    if status:
        stmt = stmt.where(Vendor.status == status)
    if province:
        stmt = stmt.where(Vendor.provinsi == province)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def update_vendor(db: AsyncSession, vendor_id: uuid.UUID, **fields) -> Vendor | None:
    vendor = await db.get(Vendor, vendor_id)
    if vendor:
        for k, v in fields.items():
            setattr(vendor, k, v)
        await db.flush()
    return vendor
