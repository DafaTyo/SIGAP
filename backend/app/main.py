"""SIGAP FastAPI app assembly."""

from __future__ import annotations

from fastapi import FastAPI

from app.api import api_router

app = FastAPI(title="SIGAP API", version="0.2.0", openapi_url="/openapi.json")
app.include_router(api_router, prefix="/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
