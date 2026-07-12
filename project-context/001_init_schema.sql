-- 001_init_schema.sql
-- SIGAP Database Initialization Script
-- Author: Kuma (Senior Enterprise Solution Architect)
-- Standard: DAMA-DMBOK, Satu Data Indonesia, UU PDP 27/2022

-- 1. EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- 2. ENCRYPTION HELPERS
-- Use a master key for PII data. In production, this should be managed via KMS.
-- We use pgp_sym_encrypt/decrypt for AES-256 encryption at rest.
CREATE OR REPLACE FUNCTION encrypt_pii(data TEXT) RETURNS BYTEA AS $$
BEGIN
    RETURN pgp_sym_encrypt(data, current_setting('app.pii_master_key', true));
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION decrypt_pii(data BYTEA) RETURNS TEXT AS $$
BEGIN
    RETURN pgp_sym_decrypt(data, current_setting('app.pii_master_key', true));
END;
$$ LANGUAGE plpgsql;

-- 3. AUDIT TRAIL ENGINE
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type TEXT NOT NULL,
    entity_id UUID NOT NULL,
    action TEXT NOT NULL,
    actor_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    timestamp TIMESTAMPTZ DEFAULT now()
);

CREATE OR REPLACE FUNCTION fn_log_audit_trail() RETURNS TRIGGER AS $$
DECLARE
    old_data JSONB := NULL;
    new_data JSONB := NULL;
    actor_id UUID := current_setting('app.current_user_id', true)::UUID;
    ip_addr INET := current_setting('app.current_ip_address', true)::INET;
BEGIN
    IF (TG_OP = 'UPDATE') THEN
        old_data := to_jsonb(OLD);
        new_data := to_jsonb(NEW);
    ELSIF (TG_OP = 'DELETE') THEN
        old_data := to_jsonb(OLD);
    ELSIF (TG_OP = 'INSERT') THEN
        new_data := to_jsonb(NEW);
    END IF;

    INSERT INTO audit_logs (entity_type, entity_id, action, actor_id, old_values, new_values, ip_address)
    VALUES (TG_TABLE_NAME, COALESCE(NEW.id, OLD.id), TG_OP, actor_id, old_data, new_data, ip_addr);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 4. CORE TABLES
-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    email_encrypted BYTEA UNIQUE NOT NULL,
    phone_encrypted BYTEA,
    role TEXT NOT NULL,
    scope_value TEXT[], -- Supporting multi-scope ABAC
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Vendors Table
CREATE TABLE IF NOT EXISTS vendors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nama_usaha TEXT NOT NULL,
    nik_penanggung_jawab_encrypted BYTEA NOT NULL,
    nib TEXT UNIQUE NOT NULL,
    alamat TEXT NOT NULL,
    province_code VARCHAR(2) NOT NULL, -- Satu Data Indonesia Standard
    city_code VARCHAR(4),
    status TEXT DEFAULT 'pending_verification',
    vendor_score FLOAT DEFAULT 0.0,
    idempotency_key VARCHAR(255) UNIQUE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Vendor Documents
CREATE TABLE IF NOT EXISTS vendor_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vendor_id UUID REFERENCES vendors(id) ON DELETE CASCADE,
    document_type TEXT NOT NULL,
    file_url TEXT NOT NULL,
    validation_status TEXT DEFAULT 'pending',
    validated_via TEXT,
    validated_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Distributions Table
CREATE TABLE IF NOT EXISTS distributions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vendor_id UUID REFERENCES vendors(id) ON DELETE CASCADE,
    jumlah_porsi INTEGER NOT NULL,
    lokasi_sekolah TEXT NOT NULL,
    location GEOGRAPHY(Point, 4326) NOT NULL,
    foto_url TEXT NOT NULL,
    reported_at TIMESTAMPTZ DEFAULT now(),
    anomaly JSONB, -- Stores probabilistic AI results
    idempotency_key VARCHAR(255) UNIQUE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Complaints Table
CREATE TABLE IF NOT EXISTS complaints (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ticket_number TEXT UNIQUE NOT NULL,
    vendor_id UUID REFERENCES vendors(id) ON DELETE CASCADE,
    kategori TEXT NOT NULL,
    deskripsi TEXT NOT NULL,
    severity TEXT DEFAULT 'rendah',
    status TEXT DEFAULT 'baru',
    resolution_notes TEXT,
    location GEOGRAPHY(Point, 4326),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- 5. GEOSPATIAL VALIDATION
-- Ensuring distributions are within a valid radius (e.g., 500m) of schools.
CREATE OR REPLACE FUNCTION fn_validate_distribution_radius() RETURNS TRIGGER AS $$
BEGIN
    -- This is a placeholder logic. In production, we compare against school_locations table.
    -- For now, we ensure the geography is valid.
    IF ST_IsValid(NEW.location::geometry) = FALSE THEN
        RAISE EXCEPTION 'Invalid geospatial coordinates provided.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 6. TRIGGERS
-- Audit Trail Triggers
CREATE TRIGGER trg_audit_vendors AFTER INSERT OR UPDATE OR DELETE ON vendors FOR EACH ROW EXECUTE FUNCTION fn_log_audit_trail();
CREATE TRIGGER trg_audit_distributions AFTER INSERT OR UPDATE OR DELETE ON distributions FOR EACH ROW EXECUTE FUNCTION fn_log_audit_trail();
CREATE TRIGGER trg_audit_complaints AFTER INSERT OR UPDATE OR DELETE ON complaints FOR EACH ROW EXECUTE FUNCTION fn_log_audit_trail();
CREATE TRIGGER trg_audit_documents AFTER INSERT OR UPDATE OR DELETE ON vendor_documents FOR EACH ROW EXECUTE FUNCTION fn_log_audit_trail();

-- Geospatial Triggers
CREATE TRIGGER trg_geo_validate_distribution BEFORE INSERT OR UPDATE ON distributions FOR EACH ROW EXECUTE FUNCTION fn_validate_distribution_radius();

-- Timestamps Triggers
CREATE OR REPLACE FUNCTION fn_update_timestamp() RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_users_timestamp BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();
CREATE TRIGGER trg_update_vendors_timestamp BEFORE UPDATE ON vendors FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();
CREATE TRIGGER trg_update_distributions_timestamp BEFORE UPDATE ON distributions FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();
CREATE TRIGGER trg_update_complaints_timestamp BEFORE UPDATE ON complaints FOR EACH ROW EXECUTE FUNCTION fn_update_timestamp();

-- 7. ROW LEVEL SECURITY (RLS)
-- Enable RLS on core data tables
ALTER TABLE vendors ENABLE ROW LEVEL SECURITY;
ALTER TABLE distributions ENABLE ROW LEVEL SECURITY;
ALTER TABLE complaints ENABLE ROW LEVEL SECURITY;

-- Admin Policy: Full Access
CREATE POLICY admin_all_vendors ON vendors FOR ALL TO PUBLIC USING (current_setting('app.current_role', true) = 'admin');
CREATE POLICY admin_all_dist ON distributions FOR ALL TO PUBLIC USING (current_setting('app.current_role', true) = 'admin');
CREATE POLICY admin_all_complaints ON complaints FOR ALL TO PUBLIC USING (current_setting('app.current_role', true) = 'admin');

-- Verifikator BGN: Full Read Access
CREATE POLICY verifikator_read_vendors ON vendors FOR SELECT TO PUBLIC USING (current_setting('app.current_role', true) = 'verifikator_bgn');

-- Pengawas Dinas: Scope-based Access (ABAC)
CREATE POLICY pengawas_scope_vendors ON vendors FOR SELECT TO PUBLIC USING (
    province_code = ANY(string_to_array(current_setting('app.current_scope', true), ','))
);

-- Vendor: Own Data Access
CREATE POLICY vendor_own_data ON distributions FOR ALL TO PUBLIC USING (
    vendor_id = (current_setting('app.current_vendor_id', true)::UUID)
);

-- 8. INDEXING
CREATE INDEX idx_vendors_province ON vendors(province_code);
CREATE INDEX idx_vendors_status ON vendors(status);
CREATE INDEX idx_dist_location ON distributions USING GIST(location);
CREATE INDEX idx_dist_reported_at ON distributions(reported_at);
CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp DESC);

-- 9. RETENTION PROCEDURES
CREATE OR REPLACE FUNCTION purge_old_audit_logs(days_limit INTEGER DEFAULT 1825) RETURNS void AS $$
BEGIN
    DELETE FROM audit_logs
    WHERE timestamp < (now() - (days_limit || ' days')::interval);
END;
$$ LANGUAGE plpgsql;
