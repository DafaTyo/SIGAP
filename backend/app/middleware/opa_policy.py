"""OPA policy evaluation middleware.

- Reads request.method, path, and user payload.
- Calls OPA server (settings.OPA_URL + settings.OPA_POLICY_PATH).
- If OPA returns false, raises PermissionDenied (403).

Reference: DESIGN.md §2.2 OPA, AGENTS.md primary directive.
"""

from __future__ import annotations

import json
import httpx

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.dependencies import settings, get_current_user


class OPAPolicyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Resolve current user (already validated by JWT)
        user = await get_current_user(request)  # type: ignore[arg-type]
        # Build OPA input payload
        payload = {
            "input": {
                "user": {
                    "id": user.id,
                    "role": user.role,
                    "scope": user.scope_value,
                },
                "request": {
                    "method": request.method,
                    "path": request.url.path,
                },
            }
        }
        opa_url = f"{settings.OPA_URL}/{settings.OPA_POLICY_PATH}"
        async with httpx.AsyncClient(timeout=2.0) as client:
            try:
                resp = await client.post(opa_url, json=payload)
                resp.raise_for_status()
                decision = resp.json().get("result", False)
            except Exception as exc:
                # Fail‑closed: deny any request if OPA cannot be reached.
                raise PermissionDenied(detail=f"OPA evaluation error: {exc}") from exc
        if not decision:
            raise PermissionDenied(detail="Policy denies this operation")
        return await call_next(request)
