"""Distribution router — /distributions endpoints per api-contract.yaml.

Endpoints implemented:
- POST / (submit report) - requires X-Idempotency-Key, async anomaly detection
- GET / (list with filtering) - ABAC scoped
- GET /{id} (detail)
- GET /{id}/metadata (audit-only metadata)
- POST /{id}/appeal (vendor appeal against flag)
"""

from __future__ import annotations
import uuid

from fastapi import APIRouter, Depends, Query, Request, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.dependencies import get_db, get_current_user
from app.dependencies.jwt_auth import UserPayload
from app.domains.distribution.schemas import (
    DistributionCreate, DistributionRead, DistributionMetadata, AppealResponse
)
from app.domains.vendor.schemas import PaginatedResponse
from app.domains.distribution import services
from app.core.exceptions import PermissionDenied

router = APIRouter()


@router.post("", response_model=DistributionRead, status_code=201)
async def submit_report(
    request: Request,
    dto: DistributionCreate,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
):
    # Capture EXIF/photo metadata from request state (set by upload handler)
    photo_taken_at = getattr(request.state, "photo_taken_at", None)
    return await services.submit_report(db, dto, user.id, photo_taken_at=photo_taken_at)


@router.get("/{report_id}", response_model=DistributionRead)
async def get_report(
    report_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
):
    return await services.get_detail(db, report_id)


@router.get("", response_model=PaginatedResponse[DistributionRead])
async def list_reports(
    vendor_id: uuid.UUID | None = Query(None),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    has_anomaly: bool | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
):
    items, total_items = await services.list_reports_service(
        db, vendor_id=vendor_id, date_from=date_from, date_to=date_to,
        has_anomaly=has_anomaly, user_scope=user.scope_value,
        limit=page_size, offset=(page - 1) * page_size,
    )
    total_pages = max((total_items + page_size - 1) // page_size, 1)
    return {
        "data": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
        },
    }


@router.get("/{report_id}/metadata", response_model=DistributionMetadata)
async def get_metadata(
    report_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
):
    # Audit-only: verifikator_bgn/pengawas_dinas/admin
    if user.role not in ("verifikator_bgn", "pengawas_dinas", "admin"):
        raise PermissionDenied(detail="Akses metadata dibatasi untuk auditor")
    return await services.get_metadata(db, report_id)


@router.post("/{report_id}/appeal", response_model=AppealResponse)
async def appeal_report(
    report_id: uuid.UUID,
    reason: str = Form(...),
    supporting_evidence: UploadFile | None = None,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
):
    # Vendor can only appeal against own reports
    if user.role != "vendor":
        raise PermissionDenied(detail="Hanya vendor yang dapat mengajukan banding")
    return await services.submit_appeal(db, report_id, user.id, reason)