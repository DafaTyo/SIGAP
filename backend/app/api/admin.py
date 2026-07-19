from fastapi import APIRouter
import uuid
router = APIRouter()

@router.post("/users")
async def create_user():
    return {"id": uuid.uuid4(), "status": "created"}
