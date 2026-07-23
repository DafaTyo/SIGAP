-- SIGAP PostgreSQL Bootstrap Script
-- Run this BEFORE alembic to enable required extensions

-- Enable PostGIS for geospatial queries
CREATE EXTENSION IF NOT EXISTS postgis;

-- Enable pgcrypto for NIK encryption (pgp_sym_encrypt/decrypt)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- After running alembic upgrade, add the GiST index and geog column:
-- These cannot be created via alembic autogenerate because they use
-- PostGIS-specific types.

-- Convert text geog column to proper PostGIS geography type
ALTER TABLE distributions
  ADD COLUMN geog geography(Point, 4326);

-- Populate geog from lat/lon for existing rows
UPDATE distributions
  SET geog = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography;

-- Create trigger to auto-populate geog on insert/update
CREATE OR REPLACE FUNCTION update_geog_from_latlon() RETURNS trigger AS $$
BEGIN
  NEW.geog := ST_SetSRID(ST_MakePoint(NEW.longitude, NEW.latitude), 4326)::geography;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_distributions_geog
  BEFORE INSERT OR UPDATE OF latitude, longitude
  ON distributions
  FOR EACH ROW
  EXECUTE FUNCTION update_geog_from_latlon();

-- GiST index for fast ST_DWithin queries
CREATE INDEX IF NOT EXISTS ix_distributions_geog
  ON distributions USING GIST (geog);

-- Idempotency cleanup: delete expired keys (run via cron daily)
-- DELETE FROM idempotency_keys WHERE expires_at < NOW();
