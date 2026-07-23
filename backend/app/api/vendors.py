"""Vendor router — /vendors endpoints per api-contract.yaml.

Endpoints:
- POST / (register vendor)
- GET / (list with filters + pagination)
- GET /{vendor_id} (detail)
- PATCH /{vendor_id} (update alamat/kontak)
- GET /{vendor_id}/nik (RESTRICTED — PII reveal)
- POST /{vendor_id}/documents (upload legal doc)
- GET /{vendor_id}/documents/{document_id}/status
- GET /{vendor_id}/documents/{document_id}/status/stream (SSE)
- POST /{vendor_id}/verify (approve/reject)
- GET /{vendor_id}/sio
- GET /{vendor_id}/score
"""

from __future__ import annotations
import uuid

from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.dependencies.jwt_auth import UserPayload
from app.domains.vendor.schemas import (
    VendorCreate, VendorUpdate, VendorRead, VendorVerifyRequest,
    PaginatedResponse, VendorNikReveal, VendorDocument,
    DocumentValidationStatus, SIODigitalRead, VendorScoreRead,
)
from app.domains.vendor import services
from app.middleware.rbac import require_permission

router = APIRouter()


@router.post("", response_model=VendorRead, status_code=201)
async def create_vendor(
    dto: VendorCreate,
    db: AsyncSession = Depends(get_db),
) -> VendorRead:
    return await services.register_vendor(db, dto)


@router.get("", response_model=PaginatedResponse[VendorRead])
@require_permission("vendors:read")
async def list_vendors(
    status: str | None = Query(None),
    province: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
) -> dict:
    items, total_items = await services.list_vendors_service(
        db, status=status, province=province, user_scope=user.scope_value,
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


@router.get("/{vendor_id}", response_model=VendorRead)
@require_permission("vendors:read")
async def get_vendor(
    vendor_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
) -> VendorRead:
    return await services.get_vendor_detail(db, vendor_id)


@router.patch("/{vendor_id}", response_model=VendorRead)
@require_permission("vendors:write")
async def patch_vendor(
    vendor_id: uuid.UUID,
    dto: VendorUpdate,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
) -> VendorRead:
    return await services.patch_vendor(db, vendor_id, dto)


@router.get("/{vendor_id}/nik", response_model=VendorNikReveal)
@require_permission("vendors:reveal")
async def reveal_vendor_nik(
    vendor_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
) -> VendorNikReveal:
    return await services.reveal_nik(db, vendor_id, user.id, user.id)


@router.post("/{vendor_id}/documents", response_model=VendorDocument, status_code=201)
@require_permission("vendors:write")
async def upload_document(
    vendor_id: uuid.UUID,
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
) -> VendorDocument:
    return await services.upload_document(db, vendor_id, document_type, file)


@router.get("/{vendor_id}/documents/{document_id}/status", response_model=DocumentValidationStatus)
@require_permission("vendors:read")
async def get_document_status(
    vendor_id: uuid.UUID,
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
) -> DocumentValidationStatus:
    return await services.get_document_status(db, document_id)


@router.get("/{vendor_id}/documents/{document_id}/status/stream")
@require_permission("vendors:read")
async def get_document_status_stream(
    vendor_id: uuid.UUID,
    document_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
):
    """SSE endpoint — returns a single event for now, real SSE streaming
    would use StreamingResponse + EventSource pattern per DATA_GOVERNANCE.md §12."""
    status = await services.get_document_status(db, document_id)
    from fastapi.responses import StreamingResponse
    import json
    data = json.dumps({
        "status": status.status,
        "validated_via": status.validated_via,
        "validated_at": status.validated_at.isoformat() if status.validated_at else None,
    })
    async def event_stream():
        yield f"data: {data}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.post("/{vendor_id}/verify", response_model=VendorRead)
@require_permission("vendors:verify")
async def verify_vendor(
    vendor_id: uuid.UUID,
    dto: VendorVerifyRequest,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
) -> VendorRead:
    return await services.verify_vendor(db, vendor_id, user.id, dto.decision, dto.notes)


@router.get("/{vendor_id}/sio", response_model=SIODigitalRead)
@require_permission("vendors:read")
async def get_vendor_sio(
    vendor_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
) -> SIODigitalRead:
    return await services.get_sio(db, vendor_id)


@router.get("/{vendor_id}/score", response_model=VendorScoreRead)
@require_permission("vendors:read")
async def get_vendor_score(
    vendor_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
) -> VendorScoreRead:
    return await services.get_vendor_score(db, vendor_id)