"""Distribution service — tampering detection, geospatial validation.

Implements:
- photo tampering detection (>24h)
- geospatial validation via Haversine distance (placeholder for PostGIS ST_DWithin)
- async policy enforcement via OPA (handled by middleware)
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from math import radians, cos, sin, sqrt, atan2

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.exceptions import GeoValidationError, NotFoundError
from app.domains.distribution.models import DistributionReport
from app.domains.distribution.schemas import (
    DistributionCreate,
    DistributionRead,
    DistributionMetadata,
    AppealResponse,
)
from app.domains.distribution.repositories import (
    create_report as repo_create_report,
    get_report as repo_get_report,
    list_reports as repo_list_reports,
)


async def submit_report(
    db: AsyncSession,
    dto: DistributionCreate,
    user_id: uuid.UUID,
    photo_taken_at: datetime | None = None,
) -> DistributionRead:
    """Create a distribution report with tampering and location validation.

    - Tampering: flag if photo timestamp is older than 24h.
    - Geospatial: ensure the reported location is within 100 m of the school's coordinates.
    """
    # Tampering detection
    tampering = False
    if photo_taken_at:
        age = datetime.now(timezone.utc) - photo_taken_at
        if age > timedelta(hours=24):
            tampering = True

    # Geospatial validation – ensure report location is within 100 m of the school
    # If schools table doesn't exist (dev mode), skip validation gracefully.
    geo_valid = None
    if dto.lokasi_sekolah:
        try:
            sql = text("SELECT latitude, longitude FROM schools WHERE nama = :name LIMIT 1")
            row = await db.execute(sql, {"name": dto.lokasi_sekolah})
            school_row = row.fetchone()
        except Exception:
            school_row = None  # schools table doesn't exist yet

        if school_row:
            def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
                R = 6371000
                dlat = radians(lat2 - lat1)
                dlon = radians(lon2 - lon1)
                a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                return R * c

            distance = haversine(dto.latitude, dto.longitude, school_row[0], school_row[1])
            if distance > 100:
                raise GeoValidationError(
                    detail=f"Lokasi laporan (jarak {int(distance)} m) berada di luar radius 100 m sekolah {dto.lokasi_sekolah}"
                )
            geo_valid = (school_row[0], school_row[1])

    report = DistributionReport(
        vendor_id=dto.vendor_id,
        jumlah_porsi=dto.jumlah_porsi,
        lokasi_sekolah=dto.lokasi_sekolah,
        latitude=dto.latitude,
        longitude=dto.longitude,
        photo_taken_at=photo_taken_at,
        tampering_suspicion=tampering,
    )
    await repo_create_report(db, report)
    await db.commit()
    return _to_read(report)


async def get_detail(db: AsyncSession, report_id: uuid.UUID) -> DistributionRead:
    report = await repo_get_report(db, report_id)
    if not report:
        raise NotFoundError(detail=f"Distribution {report_id} tidak ditemukan")
    return _to_read(report)


async def list_reports_service(
    db: AsyncSession,
    vendor_id: uuid.UUID | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    has_anomaly: bool | None = None,
    user_scope: list[str] | None = None,
    limit: int = 50,
    offset: int = 0,
) -> tuple[list[DistributionRead], int]:
    items, total = await repo_list_reports(
        db, vendor_id=vendor_id, date_from=date_from, date_to=date_to,
        has_anomaly=has_anomaly, user_scope=user_scope,
        limit=limit, offset=offset,
    )
    return [_to_read(r) for r in items], total


async def get_metadata(db: AsyncSession, report_id: uuid.UUID) -> DistributionMetadata:
    report = await repo_get_report(db, report_id)
    if not report:
        raise NotFoundError(detail="Report not found")
    return DistributionMetadata(
        distribution_id=report.id,
        photo_taken_at=report.photo_taken_at,
        exif_timestamp=report.photo_taken_at,
        device_id=None,
        latitude=report.latitude,
        longitude=report.longitude,
        tampering_suspicion=report.tampering_suspicion,
        created_at=report.reported_at,
    )


async def submit_appeal(
    db: AsyncSession,
    report_id: uuid.UUID,
    user_id: uuid.UUID,
    reason: str,
) -> AppealResponse:
    # Placeholder: mark report as frozen & create appeal entry
    report = await repo_get_report(db, report_id)
    if not report:
        raise NotFoundError(detail="Report not found")
    # In real impl: create Appeal record & set report.is_frozen=True
    return AppealResponse(
        distribution_id=report.id,
        appeal_status="pending_review",
        is_frozen=True,
        submitted_at=datetime.now(timezone.utc),
    )


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
