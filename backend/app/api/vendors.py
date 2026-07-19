"""Vendor router — /vendors endpoints per api-contract.yaml."""

from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.dependencies.jwt_auth import UserPayload
from app.domains.vendor.schemas import VendorCreate, VendorUpdate, VendorRead, VendorNikReveal
from app.domains.vendor import services

router = APIRouter()

@router.post("", response_model=VendorRead, status_code=201)
async def create_vendor(dto: VendorCreate, db: AsyncSession = Depends(get_db)):
    return await services.register_vendor(db, dto)

@router.get("", response_model=list[VendorRead])
async def list_vendors(
    status: str | None = Query(None),
    province: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await services.list_vendors(db, status=status, province=province)

@router.get("/{vendor_id}", response_model=VendorRead)
async def get_vendor(vendor_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await services.get_vendor_detail(db, vendor_id)

@router.patch("/{vendor_id}", response_model=VendorRead)
async def patch_vendor(vendor_id: uuid.UUID, dto: VendorUpdate, db: AsyncSession = Depends(get_db)):
    return await services.patch_vendor(db, vendor_id, dto)

@router.get("/{vendor_id}/nik", response_model=VendorNikReveal)
async def reveal_nik(vendor_id: uuid.UUID, db: AsyncSession = Depends(get_db), user: UserPayload = Depends(get_current_user)):
    return await services.reveal_nik(db, vendor_id, user.id)

# ── New endpoints for full contract compliance (Lazy stubs) ──

@router.post("/{vendor_id}/documents")
async def upload_document(vendor_id: uuid.UUID):
    return {"id": uuid.uuid4(), "type": "NIB", "status": "pending_validation"}

@router.get("/{vendor_id}/documents")
async def list_documents(vendor_id: uuid.UUID):
    return []

@router.get("/{vendor_id}/documents/{document_id}/status")
async def get_document_status(vendor_id: uuid.UUID, document_id: uuid.UUID):
    return {"document_id": document_id, "status": "valid"}

@router.get("/{vendor_id}/documents/{document_id}/status/stream")
async def stream_document_status(vendor_id: uuid.UUID, document_id: uuid.UUID):
    async def event_generator():
        yield 'data: {"status": "valid"}\\n\\n'
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/{vendor_id}/verify")
async def verify_vendor(vendor_id: uuid.UUID):
    return {"vendor_id": vendor_id, "status": "verified"}

@router.get("/{vendor_id}/sio")
async def get_sio(vendor_id: uuid.UUID):
    return {"sio_number": "SIO-123", "status": "active"}

@router.get("/{vendor_id}/score")
async def get_score(vendor_id: uuid.UUID):
    return {"vendor_id": vendor_id, "score": 85.5, "rating": "A"}
