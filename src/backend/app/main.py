from app.api.v1.api import api_router
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.core.config import settings

# Inisiasi app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Backend API untuk Sistem Integrasi Gizi & Akuntabilitas Pangan (SIGAP)",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler untuk konsistensi RFC 7807 (Problem Details)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "type": "https://api.sigap.id/errors/internal-server-error",
            "title": "Internal Server Error",
            "status": 500,
            "detail": "Terjadi kesalahan internal pada server.",
            "instance": request.url.path,
        }
    )

# Placeholder Routers
@app.get("/healthz", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "sigap-backend"}

# Untuk test run saja sebelum folder v1 selesai
app.include_router(api_router, prefix=settings.API_V1_STR)
