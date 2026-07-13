# TASK.md – Backend/api

## Goals
- Implement router FastAPI untuk resource utama: **vendors**, **contracts**, **auth**, **audit**.
- Terapkan **dependency injection** (`Depends`) untuk DB session, OPA enforcement, dan audit logger.
- Seluruh endpoint harus mematuhi **OpenAPI 3.1** dan menghasilkan schema yang dapat di‑generate otomatis.

## Verification Criteria
- [] Endpoint CRUD (`GET /vendors`, `POST /vendors`, `PUT /vendors/{id}`, `DELETE /vendors/{id}`) mengembalikan status yang tepat (200/201/204).
- [] Validasi request dengan **Pydantic** (field types, email format, UUID).
- [] OPA policy middleware menolak request yang tidak berizin (403).
- [] Semua endpoint terdokumentasi di `/docs` dan schema menghasilkan **OpenAPI** yang valid (`openapi-schema-validator`).
- [] Unit‑test (`pytest backend/tests/api`) mencakup semua endpoint dengan coverage ≥ 90 %.

## Status
- [ ] Pending
