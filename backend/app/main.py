from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import api_router
from app.core.exceptions import SIGAPException
from app.core.api_error import APIError
from app.middleware import (
    MiddlewareErrorWrapper, RLSSetterMiddleware, OPAPolicyMiddleware,
    IdempotencyMiddleware, RateLimitMiddleware, AuditLogMiddleware
)
from app.core.logger import configure_logging

configure_logging()

app = FastAPI(title="SIGAP API", version="0.2.0")

# Register Middlewares (Order matters – outermost first)
app.add_middleware(MiddlewareErrorWrapper)
app.add_middleware(RLSSetterMiddleware)
app.add_middleware(AuditLogMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(IdempotencyMiddleware)
app.add_middleware(OPAPolicyMiddleware)

@app.exception_handler(SIGAPException)
async def sigap_exception_handler(request: Request, exc: SIGAPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIError(code=exc.status_code, detail=exc.detail).model_dump(),
    )

app.include_router(api_router, prefix="/v1")

@app.get("/health")
async def health():
    return {"status": "ok"}
