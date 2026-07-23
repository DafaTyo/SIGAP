"""Complaint router — /complaints endpoints per api-contract.yaml.

Endpoints implemented:
- POST / (submit complaint) — public, tanpa auth (security: [])
- GET /{id} (detail) — public, akses via nomor tiket
- PATCH /{id} (update status) — verifikator_bgn/admin
- GET / (list complaints, scoped) — verifikator/pengawas/admin
"""

from __future__ import annotations
import uuid

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.dependencies.jwt_auth import UserPayload
from app.domains.complaint.schemas import ComplaintCreate, ComplaintRead, ComplaintUpdate
from app.domains.complaint import services
from app.core.exceptions import PermissionDenied
from app.domains.vendor.schemas import PaginatedResponse

router = APIRouter()


@router.post("", response_model=ComplaintRead, status_code=201)
async def submit_complaint(
    dto: ComplaintCreate,
    db: AsyncSession = Depends(get_db),
):
    """Public endpoint — no auth required per api-contract."""
    return await services.submit_complaint(db, dto)


@router.get("/{complaint_id}", response_model=ComplaintRead)
async def get_complaint(
    complaint_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Public endpoint — no auth required."""
    return await services.get_detail(db, complaint_id)


@router.patch("/{complaint_id}", response_model=ComplaintRead)
async def patch_complaint(
    complaint_id: uuid.UUID,
    dto: ComplaintUpdate,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
) -> ComplaintRead:
    if user.role not in ("verifikator_bgn", "admin"):
        raise PermissionDenied(detail="Hanya verifikator_bgn yang dapat mengupdate pengaduan")
    return await services.patch_complaint(db, complaint_id, dto)


@router.get("", response_model=PaginatedResponse[ComplaintRead])
async def list_complaints(
    status: str | None = Query(None),
    severity: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
) -> dict:
    items, total_items = await services.list_complaints(
        db, status=status, severity=severity, user_scope=user.scope_value,
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