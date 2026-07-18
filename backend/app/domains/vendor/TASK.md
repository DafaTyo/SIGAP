# 📌 Module Task Tracker: Vendor Domain (backend/app/domains/vendor)

## 🎯 Core Objective & Responsibility
- Handle vendor registration, document submission tracking, and secure PII reveal.

## 📋 Development Checklist
- [x] **Package init** – `__init__.py` created.
- [x] **Models** – `models.py` uses LargeBinary for encrypted fields.
- [x] **Schemas** – `schemas.py` defines masked response schema.
- [x] **Repository** – `repositories.py` handles DB state storage.
- [x] **Service** – `services.py` coordinates logic, NIK masking, and reveal constraints.

## 🔒 Constraints & Best Practices
- Plain NIK never exposed via standard read models.

## 📄 References
- `api-contract.yaml` – `/vendors` endpoints.
- `docs/DATA_GOVERNANCE.md` – NIK encryption specification.
