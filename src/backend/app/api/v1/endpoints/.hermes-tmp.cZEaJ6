from fastapi import APIRouter, Header
from typing import Optional

router = APIRouter()

@router.post("")
def create_complaint(x_idempotency_key: Optional[str] = Header(default=None, alias="X-Idempotency-Key")):
    return {"message": "TODO: create complaint", "idempotency_key": x_idempotency_key}

@router.get("")
def list_complaints():
    return {"data": [], "pagination": {"page": 1, "page_size": 20, "total_items": 0, "total_pages": 0}}

@router.get("/{id}")
def get_complaint(id: str):
    return {"message": "TODO: get complaint detail", "complaint_id": id}

@router.patch("/{id}")
def update_complaint(id: str):
    return {"message": "TODO: update complaint", "complaint_id": id}
