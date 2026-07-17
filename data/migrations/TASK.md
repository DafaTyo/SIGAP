# 📌 Module Task Tracker: Migrations Folder (data/migrations)

## 🎯 Core Objective & Responsibility
- Store SQL migration scripts that set up the database schema, extensions, and security infrastructure required by SIGAP.

## 📋 Development Checklist
- [x] **Migration 0001** – `0001_enable_pgcrypto_and_rls.sql` (creates extensions, `audit_logs`, RLS helpers, idempotency table).

## 🔒 Constraints & Best Practices
- Migrations must be idempotent (`CREATE EXTENSION IF NOT EXISTS`, `DO $$ … $$`).
- `audit_logs` table is append‑only; a trigger enforces immutability.
- All RLS helper functions (`current_user_id_fn`, `current_scope_fn`) must be present for `SET LOCAL` usage.

## 📄 References
- `docs/DESIGN.md` – database layer.
- `docs/DATA_GOVERNANCE.md` – audit‑log & RLS policy.
