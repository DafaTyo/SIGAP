from fastapi import APIRouter
router = APIRouter()

@router.get("/dashboard/summary")
async def get_summary():
    return {"total_vendors": 100, "total_distributions": 5000}

@router.get("/vendors/verify")
async def verify_vendor_public(nib: str = ""):
    return {"is_verified": True}
