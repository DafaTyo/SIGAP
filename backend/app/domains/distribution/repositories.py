"""Distribution repository — CRUD with pagination."""

from __future__ import annotations

import uuid
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.distribution.models import DistributionReport


async def create_report(db: AsyncSession, report: DistributionReport) -> DistributionReport:
    db.add(report)
    await db.flush()
    return report


async def get_report(db: AsyncSession, report_id: uuid.UUID) -> DistributionReport | None:
    return await db.get(DistributionReport, report_id)


async def list_reports(
    db: AsyncSession,
    vendor_id: uuid.UUID | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    has_anomaly: bool | None = None,
    user_scope: list[str] | None = None,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[DistributionReport], int]:
    # Count
    count_q = select(func.count()).select_from(DistributionReport)
    if vendor_id:
        count_q = count_q.where(DistributionReport.vendor_id == vendor_id)
    if has_anomaly is not None:
        count_q = count_q.where(DistributionReport.tampering_suspicion == has_anomaly)
    total = await db.scalar(count_q) or 0

    # Fetch
    stmt = select(DistributionReport).limit(limit).offset(offset)
    if vendor_id:
        stmt = stmt.where(DistributionReport.vendor_id == vendor_id)
    if has_anomaly is not None:
        stmt = stmt.where(DistributionReport.tampering_suspicion == has_anomaly)
    stmt = stmt.order_by(DistributionReport.reported_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all()), total


async def update_report(db: AsyncSession, report_id: uuid.UUID, **fields) -> DistributionReport | None:
    report = await db.get(DistributionReport, report_id)
    if report:
        for k, v in fields.items():
            setattr(report, k, v)
        await db.flush()
    return report
