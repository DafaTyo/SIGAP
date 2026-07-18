"""Vendor router — /vendors endpoints per api-contract.yaml."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
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
