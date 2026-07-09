from fastapi import APIRouter, Header
from typing import Optional

router = APIRouter()

@router.post("")
def create_distribution(x_idempotency_key: Optional[str] = Header(default=None, alias="X-Idempotency-Key")):
    return {"message": "TODO: create distribution report", "idempotency_key": x_idempotency_key}

@router.get("")
def list_distributions():
    return {"data": [], "pagination": {"page": 1, "page_size": 20, "total_items": 0, "total_pages": 0}}

@router.get("/{distribution_id}")
def get_distribution(distribution_id: str):
    return {"message": "TODO: get distribution detail", "distribution_id": distribution_id}

@router.post("/{id}/appeal")
def appeal_distribution(id: str):
    return {"message": "TODO: submit appeal", "distribution_id": id}
