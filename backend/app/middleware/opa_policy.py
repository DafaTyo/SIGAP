"""OPA policy evaluation middleware.

- Reads request.method, path, and user payload.
- Calls OPA server (settings.OPA_URL + settings.OPA_POLICY_PATH).
- If OPA returns false, raises PermissionDenied (403).

Reference: DESIGN.md §2.2 OPA, AGENTS.md primary directive.
"""

from __future__ import annotations
from __future__ import annotations

import json
import httpx
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import settings
from app.core.exceptions import PermissionDenied, Unauthorized
from app.dependencies.jwt_auth import get_current_user
from starlette.exceptions import HTTPException

class OPAPolicyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Public endpoints (no security) can proceed directly
        safe_paths = ["/auth/login", "/auth/me", "/auth/me/permissions", "/audit-logs", "/health"]

        # Strip /v1 prefix for safe-path matching
        check_path = request.url.path
        if check_path.startswith("/v1/"):
            check_path = "/" + check_path[len("/v1/"):]

        if request.url.path.startswith("/public/") or check_path in safe_paths:
            return await call_next(request)
            
        # Resolve current user from Authorization header
        try:
            auth_header = request.headers.get("Authorization", "")
            token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else ""
            if not token:
                raise Unauthorized(detail="Missing Bearer token")
            from app.dependencies.jwt_auth import _decode_token, UserPayload
            payload = _decode_token(token)
            user = UserPayload(
                id=str(payload.get("sub") or payload.get("id", "")),
                role=payload.get("role", ""),
                scope_type=payload.get("scope_type", ""),
                scope_value=payload.get("scope_value", []),
            )
        except Unauthorized:
            return await call_next(request)
            
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
                # Fail-open in dev mode (OPA server may not be running)
                if settings.ENV == "dev":
                    return await call_next(request)
                # Fail-closed: deny any request if OPA cannot be reached.
                raise PermissionDenied(detail=f"OPA evaluation error: {exc}") from exc
        if not decision:
            raise PermissionDenied(detail="Policy denies this operation")
        return await call_next(request)
