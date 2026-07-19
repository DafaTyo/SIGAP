from fastapi import APIRouter
router = APIRouter()

@router.post("/login")
async def login():
    return {"access_token": "mock-jwt-token", "token_type": "bearer"}

@router.get("/me")
async def me():
    return {"id": "123e4567-e89b-12d3-a456-426614174000", "role": "vendor"}

@router.get("/me/permissions")
async def permissions():
    return {"permissions": ["read:vendors", "write:distributions"]}
