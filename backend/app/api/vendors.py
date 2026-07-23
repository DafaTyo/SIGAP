
import uuid
from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, get_current_user
from app.dependencies.jwt_auth import UserPayload
from app.domains.vendor.schemas import VendorCreate, VendorUpdate, VendorRead, VendorVerifyRequest, PaginatedResponse
from app.domains.vendor import services
from app.middleware.rbac import require_permission

router = APIRouter()

@router.post("", response_model=VendorRead, status_code=201)
async def create_vendor(dto: VendorCreate, db: AsyncSession = Depends(get_db)):
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
):
    # Logika pagination ditangani di service nanti
    items, total_items = await services.list_vendors_service(db, status=status, province=province, user_scope=user.scope_value)
    return {
        "data": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": (total_items + page_size - 1) // page_size,
        },
    }

@router.post("/{vendor_id}/verify", response_model=VendorRead)
@require_permission("vendors:verify")
async def verify_vendor(
    vendor_id: uuid.UUID,
    dto: VendorVerifyRequest,
    db: AsyncSession = Depends(get_db),
    user: UserPayload = Depends(get_current_user),
):
    return await services.verify_vendor(db, vendor_id, user.id, dto.decision, dto.notes)
