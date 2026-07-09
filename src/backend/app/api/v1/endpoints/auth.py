from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login():
    return {"message": "TODO: implement JWT login"}

@router.get("/me")
def get_me():
    return {"message": "TODO: return current user"}

@router.get("/me/permissions")
def get_my_permissions():
    return {
        "role": "pengawas_dinas",
        "permissions": ["vendor:read", "distribution:read", "complaint:read"],
        "scope": {"type": "provinsi", "value": ["DKI Jakarta", "Jawa Barat"]},
    }
