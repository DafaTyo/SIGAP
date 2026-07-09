from fastapi import APIRouter, UploadFile, File, Form, Header
from typing import Optional

router = APIRouter()

@router.post("")
def create_vendor(x_idempotency_key: Optional[str] = Header(default=None, alias="X-Idempotency-Key")):
    return {"message": "TODO: create vendor", "idempotency_key": x_idempotency_key}

@router.get("")
def list_vendors():
    return {"data": [], "pagination": {"page": 1, "page_size": 20, "total_items": 0, "total_pages": 0}}

@router.get("/{vendor_id}")
def get_vendor(vendor_id: str):
    return {"message": "TODO: get vendor detail", "vendor_id": vendor_id}

@router.patch("/{vendor_id}")
def update_vendor(vendor_id: str):
    return {"message": "TODO: update vendor", "vendor_id": vendor_id}

@router.post("/{vendor_id}/documents")
def upload_vendor_document(vendor_id: str, document_type: str = Form(...), file: UploadFile = File(...)):
    return {"message": "TODO: upload vendor document", "vendor_id": vendor_id, "document_type": document_type}

@router.get("/{vendor_id}/documents/{document_id}/status")
def get_vendor_document_status(vendor_id: str, document_id: str):
    return {"status": "validating", "vendor_id": vendor_id, "document_id": document_id}

@router.post("/{vendor_id}/verify")
def verify_vendor(vendor_id: str):
    return {"message": "TODO: approve/reject vendor", "vendor_id": vendor_id}

@router.get("/{vendor_id}/sio")
def get_sio(vendor_id: str):
    return {"message": "TODO: get SIO Digital", "vendor_id": vendor_id}

@router.get("/{vendor_id}/score")
def get_vendor_score(vendor_id: str):
    return {"message": "TODO: get vendor score", "vendor_id": vendor_id}
