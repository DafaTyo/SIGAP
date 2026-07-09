from fastapi import APIRouter

router = APIRouter()
audit_router = APIRouter()

@router.post("/users")
def create_user():
    return {"message": "TODO: admin create user"}

@audit_router.get("")
def list_audit_logs():
    return {"data": []}
