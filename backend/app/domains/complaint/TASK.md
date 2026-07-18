# 📌 Module Task Tracker: Complaint Domain (backend/app/domains/complaint)

## 🎯 Core Objective & Responsibility
- Handle complaint workflow: generate ticket number, resolve severity and SLA, and manage status transitions.

## 📋 Development Checklist
- [x] **Package init** – `__init__.py` created.
- [x] **Models** – `models.py` matches Complaint spec (ticket_number, status check).
- [x] **Schemas** – `schemas.py` defines request/response formats.
- [x] **Repository** – `repositories.py` supports create/get/list/update.
- [x] **Service** – `services.py` generates SG‑YYYY‑XXXX tickets and maps severity.

## 🔒 Constraints & Best Practices
- Every status update checks domain constraints.
- Default resolution SLA set to 3 days.

## 📄 References
- `api-contract.yaml` – `/complaints` definition.
- `docs/DESIGN.md` – complaint schema layout.
