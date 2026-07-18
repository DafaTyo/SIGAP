"""API router package — mounts all domain routers."""

from fastapi import APIRouter

from app.api.vendors import router as vendor_router
from app.api.distributions import router as distribution_router
from app.api.complaints import router as complaint_router

api_router = APIRouter()
api_router.include_router(vendor_router, prefix="/vendors", tags=["Vendor"])
api_router.include_router(distribution_router, prefix="/distributions", tags=["Distribution"])
api_router.include_router(complaint_router, prefix="/complaints", tags=["Complaint"])

__all__ = ["api_router"]
