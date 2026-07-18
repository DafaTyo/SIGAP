"""Distribution service — tampering detection, geospatial validation."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.domains.distribution.models import DistributionReport
from app.domains.distribution.schemas import DistributionCreate, DistributionRead
from app.domains.distribution.repositories import create_report, get_report, list_reports


async def submit_report(db: AsyncSession, dto: DistributionCreate, photo_taken_at: datetime | None = None) -> DistributionRead:
    tampering = False
    if photo_taken_at:
        age = datetime.now(timezone.utc) - photo_taken_at
        if age > timedelta(hours=24):
            tampering = True

    report = DistributionReport(
        vendor_id=dto.vendor_id,
        jumlah_porsi=dto.jumlah_porsi,
        lokasi_sekolah=dto.lokasi_sekolah,
        latitude=dto.latitude,
        longitude=dto.longitude,
        photo_taken_at=photo_taken_at,
        tampering_suspicion=tampering,
    )
    await create_report(db, report)
    return _to_read(report)


async def get_detail(db: AsyncSession, report_id: uuid.UUID) -> DistributionRead:
    report = await get_report(db, report_id)
    if not report:
        raise NotFoundError(detail=f"Distribution {report_id} tidak ditemukan")
    return _to_read(report)


def _to_read(report: DistributionReport) -> DistributionRead:
    return DistributionRead(
        id=report.id,
        vendor_id=report.vendor_id,
        jumlah_porsi=report.jumlah_porsi,
        lokasi_sekolah=report.lokasi_sekolah,
        latitude=report.latitude,
        longitude=report.longitude,
        foto_url=report.foto_url,
        reported_at=report.reported_at,
        photo_taken_at=report.photo_taken_at,
        tampering_suspicion=report.tampering_suspicion,
    )
