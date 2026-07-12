-- 001_init_schema.sql
-- ==============================================================
-- PostgreSQL migration script for SIGAP
-- Idempotent: all objects are created IF NOT EXISTS
-- --------------------------------------------------------------

-- 1. Extensions -------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- 2. Helper functions for PII encryption -----------------------
-- NOTE: In production replace the hard‑coded key with an environment variable or vault reference.
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'encrypt_nik') THEN
        CREATE OR REPLACE FUNCTION encrypt_nik(p_nik TEXT)
        RETURNS BYTEA
        LANGUAGE sql
        AS $$SELECT pgp_sym_encrypt(p_nik, 'my_secret_key');$$;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'decrypt_nik') THEN
        CREATE OR REPLACE FUNCTION decrypt_nik(p_enc BYTEA)
        RETURNS TEXT
        LANGUAGE sql
        AS $$SELECT pgp_sym_decrypt(p_enc, 'my_secret_key');$$;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'encrypt_email') THEN
        CREATE OR REPLACE FUNCTION encrypt_email(p_email TEXT)
        RETURNS BYTEA
        LANGUAGE sql
        AS $$SELECT pgp_sym_encrypt(p_email, 'my_secret_key');$$;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'decrypt_email') THEN
        CREATE OR REPLACE FUNCTION decrypt_email(p_enc BYTEA)
        RETURNS TEXT
        LANGUAGE sql
        AS $$SELECT pgp_sym_decrypt(p_enc, 'my_secret_key');$$;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'encrypt_phone') THEN
        CREATE OR REPLACE FUNCTION encrypt_phone(p_phone TEXT)
        RETURNS BYTEA
        LANGUAGE sql
        AS $$SELECT pgp_sym_encrypt(p_phone, 'my_secret_key');$$;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'decrypt_phone') THEN
        CREATE OR REPLACE FUNCTION decrypt_phone(p_enc BYTEA)
        RETURNS TEXT
        LANGUAGE sql
        AS $$SELECT pgp_sym_decrypt(p_enc, 'my_secret_key');$$;
    END IF;
END $$;

-- 3. Core tables ------------------------------------------------

-- 3.1 Users ------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email_encrypted   BYTEA NOT NULL,
    name              TEXT NOT NULL,
    role              TEXT NOT NULL,
    province_code     TEXT NOT NULL,               -- ABAC scope
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3.2 Vendors ----------------------------------------------------
CREATE TABLE IF NOT EXISTS vendors (
    id                       UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name                     TEXT NOT NULL,
    nik_encrypted            BYTEA NOT NULL,
    nib                      TEXT,
    address                  TEXT,
    province_code            TEXT NOT NULL,              -- used by RLS
    status                   TEXT NOT NULL CHECK (status IN ('pending_verification','verified','rejected','suspended')),
    vendor_score            NUMERIC,
    idempotency_key         VARCHAR(255),
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at               TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3.3 Vendor Documents -------------------------------------------
CREATE TABLE IF NOT EXISTS vendor_documents (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vendor_id        UUID NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
    document_type   TEXT NOT NULL CHECK (document_type IN ('nik','nib','pirt','sertifikat_halal','sertifikat_hygiene')),
    file_url        TEXT NOT NULL,
    validation_status TEXT NOT NULL CHECK (validation_status IN ('pending','valid','invalid')),
    validated_via   TEXT,
    validated_at    TIMESTAMPTZ,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3.4 Distributions -----------------------------------------------
CREATE TABLE IF NOT EXISTS distributions (
    id                     UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vendor_id              UUID NOT NULL REFERENCES vendors(id) ON DELETE CASCADE,
    jumlah_porsi           INTEGER NOT NULL,
    location               GEOGRAPHY(Point,4326) NOT NULL,
    school_location        GEOGRAPHY(Point,4326) NOT NULL,   -- reference point for radius checks
    radius_meters          NUMERIC NOT NULL,
    foto_url                TEXT,
    reported_at             TIMESTAMPTZ NOT NULL DEFAULT now(),
    anomaly                JSONB,               -- probabilistic AI output
    idempotency_key        VARCHAR(255),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 3.5 Complaints -------------------------------------------------
CREATE TABLE IF NOT EXISTS complaints (
    id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticket_number     TEXT NOT NULL UNIQUE,
    vendor_id         UUID REFERENCES vendors(id) ON DELETE SET NULL,
    reporter_name    TEXT,
    category          TEXT NOT NULL CHECK (category IN ('keracunan','keterlambatan','kekurangan_porsi','kualitas_makanan','lainnya')),
    description      TEXT NOT NULL,
    severity          TEXT NOT NULL CHECK (severity IN ('rendah','sedang','tinggi','kritis')),
    status            TEXT NOT NULL CHECK (status IN ('baru','diproses','ditindaklanjuti','ditutup')),
    location          GEOGRAPHY(Point,4326),
    foto_url          TEXT,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    idempotency_key  VARCHAR(255)
);

-- 3.6 Audit Logs -------------------------------------------------
CREATE TABLE IF NOT EXISTS audit_logs (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type  TEXT NOT NULL,
    entity_id    UUID NOT NULL,
    action       TEXT NOT NULL CHECK (action IN ('CREATE','UPDATE','DELETE')),
    actor_id     UUID NOT NULL,
    old_values   JSONB,
    new_values   JSONB,
    ip_address   INET,
    timestamp    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 4. Indexes ----------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_vendors_province_code ON vendors (province_code);
CREATE INDEX IF NOT EXISTS idx_vendors_idempotency_key ON vendors (idempotency_key) WHERE idempotency_key IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS uq_vendors_idempotency_key ON vendors (idempotency_key) WHERE idempotency_key IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_distributions_vendor_id ON distributions (vendor_id);
CREATE INDEX IF NOT EXISTS idx_distributions_location_gist ON distributions USING GIST (location);
CREATE INDEX IF NOT EXISTS idx_distributions_idempotency_key ON distributions (idempotency_key) WHERE idempotency_key IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS uq_distributions_idempotency_key ON distributions (idempotency_key) WHERE idempotency_key IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_complaints_vendor_id ON complaints (vendor_id);
CREATE INDEX IF NOT EXISTS idx_complaints_location_gist ON complaints USING GIST (location);
CREATE INDEX IF NOT EXISTS idx_complaints_idempotency_key ON complaints (idempotency_key) WHERE idempotency_key IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS uq_complaints_idempotency_key ON complaints (idempotency_key) WHERE idempotency_key IS NOT NULL;

-- 5. Row‑Level Security (RLS) -----------------------------------
ALTER TABLE IF EXISTS vendors ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS distributions ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS complaints ENABLE ROW LEVEL SECURITY;

CREATE POLICY vendor_scope_policy ON vendors USING (province_code = current_setting('app.current_scope'));
CREATE POLICY distribution_scope_policy ON distributions USING (
    EXISTS (SELECT 1 FROM vendors v WHERE v.id = distributions.vendor_id AND v.province_code = current_setting('app.current_scope'))
);
CREATE POLICY complaint_scope_policy ON complaints USING (
    EXISTS (SELECT 1 FROM vendors v WHERE v.id = complaints.vendor_id AND v.province_code = current_setting('app.current_scope'))
);

-- 6. Audit‑Trail function & triggers ---------------------------
CREATE OR REPLACE FUNCTION fn_log_audit_trail() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE v_actor_id UUID; v_ip INET;
BEGIN
    v_actor_id := current_setting('app.current_user_id')::UUID;
    v_ip       := current_setting('app.current_ip')::INET;
    INSERT INTO audit_logs (entity_type, entity_id, action, actor_id, old_values, new_values, ip_address, timestamp)
    VALUES (TG_TABLE_NAME, COALESCE(NEW.id, OLD.id), TG_OP, v_actor_id,
            CASE WHEN TG_OP = 'DELETE' THEN to_jsonb(OLD) ELSE to_jsonb(OLD) END,
            CASE WHEN TG_OP = 'INSERT' THEN to_jsonb(NEW) ELSE to_jsonb(NEW) END,
            v_ip, now());
    RETURN NULL;
END;
$$;
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_audit_vendors') THEN
        CREATE TRIGGER trg_audit_vendors AFTER INSERT OR UPDATE OR DELETE ON vendors FOR EACH ROW EXECUTE FUNCTION fn_log_audit_trail();
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_audit_distributions') THEN
        CREATE TRIGGER trg_audit_distributions AFTER INSERT OR UPDATE OR DELETE ON distributions FOR EACH ROW EXECUTE FUNCTION fn_log_audit_trail();
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_audit_complaints') THEN
        CREATE TRIGGER trg_audit_complaints AFTER INSERT OR UPDATE OR DELETE ON complaints FOR EACH ROW EXECUTE FUNCTION fn_log_audit_trail();
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_audit_vendor_documents') THEN
        CREATE TRIGGER trg_audit_vendor_documents AFTER INSERT OR UPDATE OR DELETE ON vendor_documents FOR EACH ROW EXECUTE FUNCTION fn_log_audit_trail();
    END IF;
END $$;

-- 7. Distribution radius validation -------------------------------
CREATE OR REPLACE FUNCTION fn_validate_distribution_radius() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF NOT ST_DWithin(NEW.location, NEW.school_location, NEW.radius_meters) THEN
        RAISE EXCEPTION 'Distribution location out of allowed radius (%.m) from school location', NEW.radius_meters;
    END IF;
    RETURN NEW;
END;
$$;
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trg_validate_distribution_radius') THEN
        CREATE TRIGGER trg_validate_distribution_radius BEFORE INSERT OR UPDATE ON distributions FOR EACH ROW EXECUTE FUNCTION fn_validate_distribution_radius();
    END IF;
END $$;

-- 8. Retention / purge function ---------------------------------
CREATE OR REPLACE FUNCTION purge_old_audit_logs() RETURNS void LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM audit_logs WHERE timestamp < now() - INTERVAL '5 years';
END;
$$;

-- 9. Miscellaneous defaults ------------------------------------
DO $$
BEGIN
    PERFORM set_config('app.current_user_id', '00000000-0000-0000-0000-000000000000', false);
    PERFORM set_config('app.current_scope', 'default', false);
    PERFORM set_config('app.current_ip', '0.0.0.0', false);
END $$;
