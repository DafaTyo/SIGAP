# 📌 Module Task Tracker: Migrations Folder (data/migrations)

## 🎯 Core Objective & Responsibility
- Store SQL migration scripts that set up the database schema, extensions, and security infrastructure required by SIGAP.

## 📋 Development Checklist
- [x] **Migration 0001** – `0001_enable_pgcrypto_and_rls.sql` (creates extensions, `audit_logs`, RLS helpers, idempotency table).
- [x] **pgcrypto extension** – AES‑256 encryption untuk NIK (Layer 2 governance).
- [x] **PostGIS extension** – geospatial validation untuk distribusi (Layer 2 governance).
- [x] **audit_logs table** – append‑only, trigger mencegah UPDATE/DELETE (Layer 2 governance).
- [x] **RLS helper functions** – `current_user_id_fn()`, `current_scope_fn()` (Layer 2 governance).
- [x] **idempotency_keys table** – window 24 h, indexed by `expires_at` (Layer 2 governance).

## 🔒 Constraints & Best Practices
- Migrations must be idempotent (`CREATE EXTENSION IF NOT EXISTS`, `DO $$ … $$`).
- `audit_logs` table is append‑only; a trigger enforces immutability.
- All RLS helper functions (`current_user_id_fn`, `current_scope_fn`) must be present for `SET LOCAL` usage.
- Domain tables (vendors, distributions, complaints) + RLS policies akan dibuat di Layer 3.

## 📄 References
- `docs/DESIGN.md` – database layer.
- `docs/DATA_GOVERNANCE.md` – audit‑log, RLS, idempotency, PII encryption policies.
- `api-contract.yaml` – `AuditLog` schema (line 1569).
