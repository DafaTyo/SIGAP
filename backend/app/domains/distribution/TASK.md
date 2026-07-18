# 📌 Module Task Tracker: Distribution Domain (backend/app/domains/distribution)

## 🎯 Core Objective & Responsibility
- Handle distribution reports: log porsi, geolocation coords, photo meta, and validate tampering.

## 📋 Development Checklist
- [x] **Package init** – `__init__.py` created.
- [x] **Models** – `models.py` matches Distribution spec.
- [x] **Schemas** – `schemas.py` defines request/response formats.
- [x] **Repository** – `repositories.py` supports create/get/list.
- [x] **Service** – `services.py` calculates photo age and flags tampering.

## 🔒 Constraints & Best Practices
- `photo_taken_at` difference of > 24 hours triggers `tampering_suspicion`.

## 📄 References
- `api-contract.yaml` – `/distributions` endpoints.
- `docs/DATA_GOVERNANCE.md` – tampering check definition.
