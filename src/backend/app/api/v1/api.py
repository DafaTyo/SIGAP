from fastapi import APIRouter

from app.api.v1.endpoints import admin, auth, complaints, distributions, public, vendors

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(vendors.router, prefix="/vendors", tags=["Vendor"])
api_router.include_router(distributions.router, prefix="/distributions", tags=["Distribution"])
api_router.include_router(complaints.router, prefix="/complaints", tags=["Complaint"])
api_router.include_router(public.router, prefix="/public", tags=["Public"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(admin.audit_router, prefix="/audit-logs", tags=["Admin"])
