# 📌 Module Task Tracker: Exceptions Package (backend/app/exceptions)

## 🎯 Core Objective & Responsibility
- Menyimpan **custom FastAPI HTTPException** subclasses yang dipakai di seluruh aplikasi (mis. `VendorNotFound`, `PermissionDenied`, `InvalidDocument`).
- Mempermudah re‑use dan konsistensi pesan error serta kode status.

## 📋 Development Checklist
- [ ] **Package init** – `__init__.py` yang meng‑export semua exception class.
- [ ] **Define Exceptions** – `exceptions.py`
  - **Classes:**
    - `VendorNotFound(HttpException)` – 404
    - `DocumentValidationFailed(HttpException)` – 422
    - `PermissionDenied(HttpException)` – 403
    - `RateLimitExceeded(HttpException)` – 429
    - `IdempotencyConflict(HttpException)` – 409
  - **Each class** harus menerima `detail: str` dan optional `headers: dict`.
- [ ] **Write Exception README** – contoh penggunaan `raise VendorNotFound(detail="Vendor not found")` di service layer.

## 🔒 Constraints & Best Practices
- **Never expose raw stack trace** – set `detail` dengan pesan yang user‑friendly.
- **All exceptions** harus dipanggil melalui `raise` di service atau router, **bukan** di middleware.
- **Testing:** Pastikan setiap exception menghasilkan JSON dengan fields `detail` dan `status_code` di test suite.

## 📄 References
- `api-contract.yaml` – definisi error response (`components/responses/BadRequest`, `Unauthorized`, `Forbidden`).
- `docs/DESIGN.md` – bagian *Error handling & audit*.

---

**Instruksi Eksplisit:** Tidak ada kode Python yang boleh dibuat sampai semua item checklist di atas ditandai selesai.
