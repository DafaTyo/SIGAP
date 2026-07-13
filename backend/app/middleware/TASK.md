# TASK.md – Backend/middleware

## Goals
- Implement *global* FastAPI middleware stack:
  1. **CORS** – allowed origins from env.
  2. **GZipMiddleware** – compress response > 500 KB.
  3. **SecurityHeadersMiddleware** – add `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`.
  4. **RequestIDMiddleware** – generate `X-Request-ID` (UUID4) per request.
  5. **OPAEnforcementMiddleware** – evaluate policy before route handler; return **403** bila deny.
  6. **AuditLoggingMiddleware** – log request/response metadata & policy decision ke tabel `vendor_audit`.
- Middleware harus **configurable** via env (`MIDDLEWARE_ENABLE_LOGGING=true` dll.)
- Pastikan middleware tidak mempengaruhi performa (> 2 ms overhead per request).

## Verification Criteria
- [] Semua middleware ter‑register di `app/main.py` menggunakan `add_middleware`.
- [] Unit‑test (`pytest backend/tests/middleware`) memverifikasi masing‑middleware (CORS header, GZip size, security headers, request‑id presence, OPA decision, audit entry).
- [] Load test (`locust` atau `k6`) menunjukkan rata‑rata latency tambahan < 2 ms.
- [] CI menjalankan `pytest backend/tests/middleware` dan coverage ≥ 90 %.
- [] Dokumentasi di `docs/MIDDLEWARE.md` menjelaskan urutan, env vars, dan contoh log entry.

## Status
- [ ] Pending
