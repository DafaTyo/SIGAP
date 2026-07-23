# Data Governance for SIGAP

---

## 1. Purpose & Scope
This document defines the data governance framework for **SIGAP** (Sistem Informasi Gubernur Aplikasi Pengadaan) to ensure that data is managed, protected, and used in compliance with:
- **DAMA‑DMBOK** (Data Management Body of Knowledge) best‑practice framework.
- **Peraturan Pemerintah** and **UU Perlindungan Data Pribadi (UU PDP)** of Indonesia.
- **Satu Data Indonesia** (National Data Governance strategy) and related SDI (Standard Data Interchange) specifications.
- Internal architectural tenets of SIGAP: modular monolith, PostgreSQL RLS + PostGIS, OPA/CASL, and Next.js BFF.

---

## 2. Governance Pillars (Aligned with DAMA‑DMBOK)
| Pillar | Description | SIGAP Implementation |
|---------|-------------|----------------------|
| **Data Stewardship** | Role‑based custodianship of data domains. | Each module (Vendor, Distribution, Complaint) has a designated Data Steward responsible for data quality, metadata, and access requests. |
| **Data Architecture** | Logical & physical models, storage, and integration. | PostgreSQL schema with UUID PKs, `pgcrypto` encryption, PostGIS geography types; OPA policies for ABAC; Next.js BFF for API exposure. |
| **Data Quality Management** | Rules, profiling, monitoring, remediation. | Validation layers in FastAPI (pydantic models) and BFF; periodic data quality jobs (Hermes cron) that flag anomalies using AI scoring. |
| **Metadata Management** | Cataloging, lineage, classification. | Central metadata table `metadata_catalog` storing column definitions, data type, sensitivity classification (Public/Private/Confidential), source system, and SDI code mappings. |
| **Data Security & Privacy** | Controls for confidentiality, integrity, availability. | Row‑Level Security (RLS) with `SET LOCAL app.current_user_id`; `pgcrypto` AES‑256 encryption for PII columns; dynamic masking in BFF; OPA policies for attribute‑based access. |
| **Data Lifecycle & Retention** | Creation → Usage → Archival → Destruction. | Retention policies enforced via scheduled Hermès jobs: audit logs >5 yr → cold storage; inactive vendors >3 yr → anonymized/removed; compliance with principle of data minimisation. |
| **Audit & Traceability** | Immutable logging of data changes. | `AuditMiddleware` captures `old_value`, `new_value`, `actor_id`, `ip_address`, `timestamp`. Audit entries stored in `audit_logs` table; immutable via append‑only partitioning. |
| **Compliance & Risk Management** | Alignment with regulations & standards. | Periodic compliance checks against UU PDP, Satu Data Indonesia, and internal policies; automated reports generated for regulator audits. |

---

## 3. Privacy & Personal Data Handling (UU PDP)
1. **PII Classification**
   - **NIK** – Confidential
   - **Email / Phone** – Private
   - **Nama, Alamat** – Private
2. **Encryption at Rest**
   - Columns marked confidential are stored encrypted using PostgreSQL `pgcrypto` (`AES-256`), e.g., `nik_encrypted BYTEA`.
3. **Dynamic Masking in BFF**
   - Masking pattern `3175********1234` applied for NIK; email shown as `user***@domain.com`.
4. **Response Masking Policy**
   - Semua endpoint yang meng‑embalikan NIK **harus** mengembalikan versi *masked* (`3175********1234`). Kolom mentah `nik_encrypted` **tidak pernah** dikirim ke client layer.
   - **Schema Separation**:
     - `vendor_public` – hanya field yang boleh dilihat publik (nama, status, lokasi, NIK_masked).
     - `vendor_admin` – menyimpan `nik_encrypted`, dokumen lengkap, metadata internal. Penggunaan schema dipilih oleh FastAPI dependency `require_schema(role)`.
5. **Consent & Purpose Limitation**
   - Data collection consent recorded in `user_consent` table; purpose codes mapped to SDI taxonomy.
6. **Data Subject Rights**
   - Endpoints for **access**, **rectification**, and **erasure** implemented per UU PDP, routed through BFF with audit logging.

---

## 4. Data Sovereignty & Localisation
- All data resides in an **Indonesia‑based data centre**.
- No cross‑border data transfer without explicit user consent and contractual safeguards.
- Use of ISO‑27001‑compliant storage and encryption meets governmental requirements.

---

## 5. Geospatial & Radius Validation
- **Geospatial Data** uses `PostGIS` `geography(Point,4326)`; region codes follow **BPS Kode Wilayah** (province, kabupaten, kecamatan, desa).
- **Radius Tolerance Mechanism**
  - Parameter `radius_tolerance_meters` (default **50 m**) added to validation logic.
  - Validation uses `ST_DWithin` with tolerance; jika jarak diluar toleransi ±10 % maka sistem memberi **warning flag** dan menandai untuk verifikasi manual.
  - Semua perubahan radius disimpan di tabel `distribution_audit` untuk traceability.
- **SDI Integration**: Export/import utilities produce CSV/JSON adhering to **Satu Data** schemas, facilitating interoperability with other government systems.

---

## 6. Metadata & Photo Timestamp
|- New column `photo_taken_at TIMESTAMP WITH TIME ZONE` added to `distributions` table.
|- **Tampering Detection**: Jika `photo_taken_at` lebih lama dari `created_at` lebih dari **24 jam**, otomatis flag `tampering_suspicion = true`.
|- Endpoint `/distributions/{id}/metadata` menyediakan metadata lengkap (EXIF, capture time, lokasi) kepada auditor.

---

## 7. Access Control (OPA / ABAC)
- Policies expressed in Rego evaluate attributes: `role`, `scope`, `region_code`.
- Example policy snippet (stored in `opa/policies/sgp.rego`):
```rego
package sigap.auth
allow {
  input.user.role == "auditor"
  input.user.region_code == data.resource.region_code
}
```
- FastAPI dependency injects `current_user` and `current_scope`; RLS context set accordingly.
- **RLS Reset Middleware** (`RLSResetMiddleware`) ensures `SET LOCAL` is cleared / reset at the end of each request, preventing leakage across pooled connections.

---

## 7. Audit Trail & Immutable Logging
- **Audit Table** (`audit_logs`): `id UUID PK`, `entity VARCHAR`, `entity_id UUID`, `action VARCHAR`, `old_value JSONB`, `new_value JSONB`, `actor_id UUID`, `ip_address INET`, `created_at TIMESTAMP WITH TIME ZONE`.
- **Triggers** automatically populate audit entries on INSERT/UPDATE/DELETE for all core tables.
- **Tamper‑evidence**: Table is partitioned by month and **append‑only**; `pg_switch_wal` ensures WAL archival.

---

## 8. Data Quality & AI Anomaly Detection
- **Batch jobs** (Hermes cron) run daily to compute data quality metrics (completeness, validity, uniqueness).
- **AI anomaly service** (FastAPI `/anomaly/detect`) returns:
  ```json
  {
    "score": 0.93,
    "confidence": 0.98,
    "flag": true,
    "detected": "unusual vendor price spike",
    "details": "..."
  }
  ```
- Anomalies are logged to `anomaly_events` and notified to stewards.

---

## 9. Retention & Archival Policies
| Data Type | Retention Period | Action After Expiry |
|-----------|-------------------|----------------------|
| Audit Logs | 5 years | Move to cold storage (object store) |
| Vendor Records (inactive >3 yr) | 3 years | Anonymize NIK, delete personal fields |
| Distribution Reports | 2 years | Archive, keep aggregated stats |
| Complaint Records | 7 years | Retain for regulatory compliance |

---

## 10. Governance Operations & Roles
- **Data Governance Council** – senior leadership overseeing policy updates.
- **Data Stewards** – domain owners ensuring quality & compliance.
- **Security Officer** – reviews RLS/OPA policies, encryption keys rotation.
- **Privacy Officer** – handles data subject request workflows.
- **AI Ethics Lead** – validates anomaly detection outputs and bias.

---

## 11. Idempotency Enforcement
- Header `X-Idempotency-Key` is **mandatory** for all state‑changing operations (`POST`, `PATCH`, `DELETE`).
- Expected format: UUID v4 (ex: `550e8400-e29b-41d4-a716-446655440000`).
- FastAPI middleware rejects any request missing the header or with a duplicate key within a 24‑hour window.

---

## 12. Real‑time Updates (SSE / WebSocket)
- Document upload workflow triggers an async task (Celery/ARQ).
- Progress is streamed to the client via **WebSocket** channel `ws://api.sigap.gov/docs/status/{upload_id}` (alternatively `EventSource` for SSE).
- Removes heavy client‑side polling and mitigates DDoS risk from repeated status requests.

---

## 13. Monitoring & Reporting
- **Hermes Cron Jobs** generate weekly compliance dashboards stored in `reports/compliance_*`.
- **OPA Policy Evaluation Logs** are streamed to a central logging system (ELK) for real‑time monitoring.
- **Security Incident Response** procedures defined in `SECURITY_INCIDENT_RESPONSE.md`.

---

*Document version: 1.1 – 12 July 2026*