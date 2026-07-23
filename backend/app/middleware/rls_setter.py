"""FastAPI middleware that sets PostgreSQL RLS variables per request.

Workflow:
  1. Depends on get_current_user (JWT) – already validated.
  2. Opens a DB session (via get_db) and executes SET LOCAL statements.
  3. Stores session in request.state.db for downstream handlers.
  4. After response, calls reset_rls_context to clear locals.

References:
  - DESIGN.md §2.1 Row‑Level Security
  - DATA_GOVERNANCE.md §7 RLS reset
  - middleware/TASK.md checklist
"""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.dependencies import get_db
from sqlalchemy import text


class RLSSetterMiddleware(BaseHTTPMiddleware):
    """Inject RLS variables into the DB session for the current request.

    Must be placed **before** any DB query execution.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Resolve user from Authorization header
        try:
            auth_header = request.headers.get("Authorization", "")
            token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else ""
            if not token:
                return await call_next(request)
            from app.dependencies.jwt_auth import _decode_token, UserPayload
            payload = _decode_token(token)
            user = UserPayload(
                id=str(payload.get("sub") or payload.get("id", "")),
                role=payload.get("role", ""),
                scope_type=payload.get("scope_type", ""),
                scope_value=payload.get("scope_value", []),
            )
        except Exception:
            return await call_next(request)
        # Open a DB session (async)
        async for db in get_db(request):
            # Set locals – SQLite doesn't support SET LOCAL (PostgreSQL only)
            # These are silently skipped on non-PostgreSQL dialects.
            dialect = db.bind.dialect.name if db.bind else ""
            if dialect == "postgresql":
                await db.execute(
                    text("SET LOCAL app.current_user_id = :uid"),
                    {"uid": user.id},
                )
                await db.execute(
                    text("SET LOCAL app.current_scope = :scope"),
                    {"scope": ",".join(user.scope_value) if isinstance(user.scope_value, list) else user.scope_value},
                )
            # Attach session to request.state for downstream code
            request.state.db = db
            # Continue down the stack
            response = await call_next(request)
            # Reset locals – important for pooled connections
            if dialect == "postgresql":
                await db.execute(text("RESET app.current_user_id"))
                await db.execute(text("RESET app.current_scope"))
            return response
        # Fallback – should never reach here
        return Response(status_code=500, content="RLS middleware failed to acquire DB session")
