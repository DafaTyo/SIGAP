-- Migration: 0001_enable_pgcrypto_and_rls.sql
-- Purpose : Enable pgcrypto, PostGIS; create audit_logs table;
--           define app_user role; add RLS infrastructure.
-- Idempotent: all statements use IF NOT EXISTS / CREATE OR REPLACE.
-- Reference : DATA_GOVERNANCE.md §3 (pgcrypto), §7 (audit), §5 (PostGIS)
--             api-contract.yaml: AuditLog schema (line 1569)

-- ── Extensions ──────────────────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS postgis;

-- ── Application role (no direct login) ──────────────────────────────────────
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'app_user') THEN
        CREATE ROLE app_user NOLOGIN;
    END IF;
END;
$$;

-- ── audit_logs (append-only) ─────────────────────────────────────────────────
-- Fields match api-contract.yaml AuditLog schema (line 1569–1597).
CREATE TABLE IF NOT EXISTS audit_logs (
    id           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_id     UUID        NOT NULL,
    action       TEXT        NOT NULL
                             CHECK (action IN ('CREATE', 'UPDATE', 'DELETE', 'PII_REVEAL')),
    entity_type  TEXT        NOT NULL,
    entity_id    UUID,
    old_values   JSONB,
    new_values   JSONB,
    ip_address   INET,
    request_id   UUID,
    timestamp    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Append-only guard: block UPDATE and DELETE on audit_logs
CREATE OR REPLACE FUNCTION prevent_audit_mutation()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'audit_logs is append-only — direct mutations forbidden';
END;
$$;

DROP TRIGGER IF EXISTS audit_no_update ON audit_logs;
CREATE TRIGGER audit_no_update
    BEFORE UPDATE OR DELETE ON audit_logs
    FOR EACH ROW EXECUTE FUNCTION prevent_audit_mutation();

-- ── RLS helper functions ─────────────────────────────────────────────────────
-- current_user_id() and current_scope() wrap SET LOCAL variables.
-- Domain tables will use USING (created_by = current_user_id_fn()).
CREATE OR REPLACE FUNCTION current_user_id_fn()
RETURNS UUID LANGUAGE sql STABLE AS $$
    SELECT current_setting('app.current_user_id', true)::UUID;
$$;

CREATE OR REPLACE FUNCTION current_scope_fn()
RETURNS TEXT LANGUAGE sql STABLE AS $$
    SELECT current_setting('app.current_scope', true);
$$;

-- ── Idempotency table ────────────────────────────────────────────────────────
-- Stores (key, response_body) pairs with 24-hour TTL via pg_cron or app-level purge.
-- DATA_GOVERNANCE.md §11: window 24 h.
CREATE TABLE IF NOT EXISTS idempotency_keys (
    key          TEXT        PRIMARY KEY,
    response     JSONB       NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at   TIMESTAMPTZ NOT NULL
);

-- Index to speed up expired key cleanup
CREATE INDEX IF NOT EXISTS ix_idempotency_expires ON idempotency_keys (expires_at);
