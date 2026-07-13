# TASK‑BE‑009‑01 – Pydantic DTOs for API Input/Output

## Goals
- Separate Pydantic models used for request validation (`CreateVendorDTO`, `UpdateVendorDTO`) from ORM models (`Vendor`).
- Ensure DTOs contain only fields that should be exposed to the client (no internal IDs, timestamps unless explicitly required).
- Provide `from_orm` compatibility for easy conversion from ORM objects to response DTOs.
- Add comprehensive schema documentation (description, examples) so that OpenAPI generated docs are clear.

## Verification Criteria
- [] DTO files live under `app/schemas/` with clear naming (`*_dto.py`).
- [] Each DTO includes `Config.orm_mode = True` for ORM conversion.
- [] Unit test `tests/schemas/test_dto.py` validates that:
  - Invalid payloads raise `ValidationError` with appropriate messages.
  - Valid ORM objects can be converted to DTOs via `DTO.from_orm`.
  - OpenAPI schema includes description/examples.
- [] CI pipeline runs DTO tests and fails if any validation rule is missing.

## Status
- [] Pending