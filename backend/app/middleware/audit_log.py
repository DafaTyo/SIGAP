"""Global audit‑log middleware.

Captures:
  - request.method, path, user.id (if any)
  - old/new values (requires domain services to set request.state.audit_payload)
  - stores row in `audit_logs` table (append‑only).

Reference: DATA_GOVERNANCE.md §8 Audit Trail.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.dependencies import get_db


class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Resolve user if present (may be None for public endpoints)
        user_id = getattr(request.state, "user", None)
        if user_id:
            user_id = getattr(user_id, "id", None)
        # Capture request metadata
        start = datetime.now(timezone.utc)
        # Continue request
        response = await call_next(request)
        end = datetime.now(timezone.utc)
        # Build payload – domain code can set request.state.audit_payload = {...}
        audit_payload = getattr(request.state, "audit_payload", None)
        if audit_payload:
            async for db in get_db():
                await db.execute(
                    """
                    INSERT INTO audit_logs (
                        id, actor_id, action, entity_type, entity_id,
                        old_values, new_values, ip_address, request_id, timestamp
                    ) VALUES (
                        :id, :actor, :action, :entity_type, :entity_id,
                        :old, :new, :ip, :req_id, :ts
                    )
                    """,
                    {
                        "id": str(uuid.uuid4()),
                        "actor": user_id,
                        "action": audit_payload.get("action"),
                        "entity_type": audit_payload.get("entity_type"),
                        "entity_id": audit_payload.get("entity_id"),
                        "old": json.dumps(audit_payload.get("old")),
                        "new": json.dumps(audit_payload.get("new")),
                        "ip": request.client.host,
                        "req_id": str(uuid.uuid4()),
                        "ts": end,
                    },
                )
                await db.commit()
        return response
