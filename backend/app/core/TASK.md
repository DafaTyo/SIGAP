# 📌 Module Task Tracker: Core Package (backend/app/core)

## 🎯 Core Objective & Responsibility
- Provide global configuration, structured logging, and base exception hierarchy for the SIGAP backend.

## 📋 Development Checklist
- [x] **Package init** – `__init__.py` placeholder.
- [x] **Config** – `config.py` implemented (pydantic‑settings, env vars).
- [x] **Logger** – `logger.py` implemented (structlog JSON logger).
- [x] **Exceptions** – `exceptions.py` implemented (SIGAPException subclasses).

## 🔒 Constraints & Best Practices
- Settings must be loaded exclusively via environment variables; no hard‑coded secrets.
- Logger output must be valid JSON with mandatory fields (`timestamp`, `level`, `module`, `event`, optional `request_id`).
- All exception classes inherit from `SIGAPException` and expose a `detail` message.

## 📄 References
- `api-contract.yaml` – response status‑code mapping.
- `docs/DESIGN.md` – logging & security architecture.
- `docs/DATA_GOVERNANCE.md` – PII handling policy.
