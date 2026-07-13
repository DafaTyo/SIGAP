# TASK.md – Backend/exceptions

## Goals
- Definisikan **custom exception hierarchy** yang konsisten dengan standar **HTTP status codes** dan **application‑specific error codes**.
- Buat **FastAPI exception handlers** yang meng‑transform `AppError` menjadi JSON response (`{"error": "...", "code": "..."}`).
- Pastikan semua exception memiliki **logging** ter‑centralized (menggunakan logger dari `core`).

## Verification Criteria
- [] `AppError` base class dengan atribut `status_code`, `detail`, `error_code`.
- [] Sub‑classes: `ValidationError`, `AuthError`, `PermissionError`, `NotFoundError`, `DatabaseError`.
- [] Exception handler (`@app.exception_handler(AppError)`) meng‑return `JSONResponse` dengan schema yang tervalidasi.
- [] Unit‑test memverifikasi mapping exception → HTTP response (status, body) dan logging output.
- [] Coverage ≥ 85 % pada folder `exceptions`.

## Status
- [ ] Pending
