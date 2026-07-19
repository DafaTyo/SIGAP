"""API router package — mounts all domain routers."""

from fastapi import APIRouter

from app.api.vendors import router as vendor_router
from app.api.distributions import router as distribution_router
from app.api.complaints import router as complaint_router
from app.api.auth import router as auth_router
from app.api.admin import router as admin_router
from app.api.public import router as public_router
from app.api.audit import router as audit_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(vendor_router, prefix="/vendors", tags=["Vendor"])
api_router.include_router(distribution_router, prefix="/distributions", tags=["Distribution"])
api_router.include_router(complaint_router, prefix="/complaints", tags=["Complaint"])
api_router.include_router(admin_router, prefix="/admin", tags=["Admin"])
api_router.include_router(public_router, prefix="/public", tags=["Public"])
api_router.include_router(audit_router, prefix="/audit-logs", tags=["Audit"])

__all__ = ["api_router"]
