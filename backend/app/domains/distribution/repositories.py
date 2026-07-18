"""Distribution repository."""

from __future__ import annotations

import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.distribution.models import DistributionReport


async def create_report(db: AsyncSession, report: DistributionReport) -> DistributionReport:
    db.add(report)
    await db.flush()
    return report


async def get_report(db: AsyncSession, report_id: uuid.UUID) -> DistributionReport | None:
    return await db.get(DistributionReport, report_id)


async def list_reports(db: AsyncSession, vendor_id: uuid.UUID | None = None) -> list[DistributionReport]:
    stmt = select(DistributionReport)
    if vendor_id:
        stmt = stmt.where(DistributionReport.vendor_id == vendor_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())
