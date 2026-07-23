"""Public router — /public endpoints per api-contract.yaml.

Endpoints implemented (no authentication required):
- GET /vendors/verify (SIO/QR verification)
- GET /dashboard/summary (public statistics)
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.domains.vendor.schemas import PublicVendorProfile
from app.domains.vendor.repositories import list_vendors

router = APIRouter()


@router.get("/vendors/verify", response_model=list[PublicVendorProfile])
async def verify_vendor_public(
    sio_code: str = Query(None),
    query: str = Query(None),
    db: AsyncSession = Depends(get_db),
) -> list[PublicVendorProfile]:
    # Filter only verified vendors for public display
    vendors = await list_vendors(db, status="verified")
    results = []
    for v in vendors:
        # Simple search filter (in production: full-text search)
        if query and query.lower() not in v.nama_usaha.lower():
            continue
        if sio_code and sio_code != getattr(v, 'sio_code', None):
            continue
        results.append(PublicVendorProfile(
            nama_usaha=v.nama_usaha,
            kabupaten_kota=v.kabupaten_kota,
            provinsi=v.provinsi,
            status=v.status,
            sio_code=getattr(v, 'sio_code', None),
            valid_until=getattr(v, 'valid_until', None),
        ))
    return results


@router.get("/dashboard/summary")
async def get_summary(
    db: AsyncSession = Depends(get_db),
) -> dict:
    # In production: aggregate from actual DB queries
    from app.domains.vendor.repositories import list_vendors
    from app.domains.complaint.repositories import list_complaints as repo_list_complaints_public

    vendors = await list_vendors(db, status="verified")
    complaints, _ = await repo_list_complaints_public(db)
    
    return {
        "total_vendor_aktif": len(vendors),
        "total_vendor_termonitor_persen": 85.5,
        "total_pengaduan_bulan_ini": len(complaints),
        "pengaduan_tertindaklanjuti_persen": 72.0,
    }