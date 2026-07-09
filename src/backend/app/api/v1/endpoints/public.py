from fastapi import APIRouter

router = APIRouter()

@router.get("/vendors/verify")
def verify_public_vendor():
    return {"data": []}

@router.get("/dashboard/summary")
def public_dashboard_summary():
    return {
        "total_vendor_aktif": 0,
        "total_vendor_termonitor_persen": 0,
        "total_pengaduan_bulan_ini": 0,
        "pengaduan_tertindaklanjuti_persen": 0,
    }
