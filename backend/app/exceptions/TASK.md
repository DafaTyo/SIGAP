# 📌 Module Task Tracker: Exceptions Package (backend/app/exceptions)

## 🎯 Core Objective & Responsibility
- Provide a thin re‑export layer for domain‑specific exception classes used throughout the application.

## 📋 Development Checklist
- [x] **Package init** – `__init__.py` re‑exports all exception symbols.
- [x] **Exceptions module** – `exceptions.py` with concrete classes (`VendorNotFound`, `PermissionDenied`, etc.).

## 🔒 Constraints & Best Practices
- All exceptions subclass `SIGAPException` (which itself subclasses FastAPI `HTTPException`).
- Each exception must carry an appropriate HTTP status code matching `api-contract.yaml`.

## 📄 References
- `api-contract.yaml` – response definitions.
- `docs/DESIGN.md` – error handling strategy.
