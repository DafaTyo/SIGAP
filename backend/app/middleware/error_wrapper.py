"""Middleware error wrapper – catches SIGAPException raised by inner middleware.

Starlette's BaseHTTPMiddleware does NOT pass exceptions raised inside middleware
through FastAPI's @app.exception_handler. This wrapper sits at the outermost
layer and converts them to proper JSON responses.

Newer Starlette wraps inner middleware exceptions inside ExceptionGroup via
anyio TaskGroup, so we need to catch both SIGAPException and ExceptionGroup.
"""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.exceptions import SIGAPException
from app.core.api_error import APIError


class MiddlewareErrorWrapper(BaseHTTPMiddleware):
    """Wrap all downstream middleware so SIGAPException becomes a proper JSON response."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except SIGAPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content=APIError(code=exc.status_code, detail=exc.detail).model_dump(),
            )
        except ExceptionGroup as eg:
            # Starlette 0.42+ wraps middleware exceptions inside ExceptionGroup
            sigap = self._find_sigap(eg)
            if sigap:
                return JSONResponse(
                    status_code=sigap.status_code,
                    content=APIError(code=sigap.status_code, detail=sigap.detail).model_dump(),
                )
            raise

    @staticmethod
    def _find_sigap(exc: BaseException) -> SIGAPException | None:
        """Walk an ExceptionGroup to find the first SIGAPException."""
        if isinstance(exc, SIGAPException):
            return exc
        if isinstance(exc, BaseExceptionGroup):
            for e in exc.exceptions:
                found = MiddlewareErrorWrapper._find_sigap(e)
                if found:
                    return found
        return None