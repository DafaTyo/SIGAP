# TASK.md – Backend/schemas

## Goals
- Pisahkan **Pydantic schemas** (request/response DTO) dari ORM model untuk menjaga **separation of concerns**.
- Setiap resource (`Vendor`, `Contract`, `User`) memiliki schema: `Create`, `Read`, `Update`.
- Pastikan schema mendukung **OpenAPI** auto‑generation dan **validation** yang ketat (email regex, UUID format, enum values).

## Verification Criteria
- [] Semua schema memiliki field dengan tipe yang tepat dan `Field(..., description="…")` untuk dokumentasi.
- [] `VendorRead` menyembunyikan kolom sensitif (mis. `secret_key`).
- [] Unit‑test (`pytest backend/tests/schemas`) memverifikasi validasi (invalid email -> ValidationError, etc.).
- [] Coverage ≥ 85 % pada folder `schemas`.
- [] OpenAPI docs (`/docs`) menampilkan schema dengan contoh nilai.

## Status
- [ ] Pending
