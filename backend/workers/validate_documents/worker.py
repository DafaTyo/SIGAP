"""Asynchronous background worker for legal document validation.

Simulates external OSS/BPOM API check and updates DB status.
"""

from __future__ import annotations

import asyncio
import uuid


async def validate_document(document_id: uuid.UUID) -> dict[str, str]:
    """Validate document asynchronously.

    ponytail: simulated mock validation — replace with httpx call to OSS/BPOM in prod.
    """
    await asyncio.sleep(1)  # Simulate network latency
    return {
        "document_id": str(document_id),
        "status": "valid",
        "validated_via": "Mock OSS API",
    }


if __name__ == "__main__":
    # Self-check
    res = asyncio.run(validate_document(uuid.uuid4()))
    assert res["status"] == "valid"
    print("Worker self-check OK:", res)
