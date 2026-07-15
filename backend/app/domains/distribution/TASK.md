# 📌 Module Task Tracker: Distribution Domain (backend/app/domains/distribution)

## 🎯 Core Objective & Responsibility
- Mengelola entitas **DistributionReport** dan logika bisnis terkait pelaporan distribusi harian.
- Menyediakan **anomali detection** hook (akan dipanggil oleh worker) dan **geospasial validation** menggunakan PostGIS.
- Menjamin integritas data melalui **idempotency** dan **rate‑limit**.

## 📋 Development Checklist
- [ ] **Package init** – `__init__.py` (expose modul).
- [ ] **Model** – `models.py`
  - **Class:** `DistributionReport`
  - **Fields:** `id (UUID)`, `vendor_id (FK)`, `report_date`, `porsi`, `photo_path`, `photo_taken_at`, `geo_point (GEOGRAPHY)`, `anomaly_score`, `risk_flag`, `created_at`, `updated_at`.
  - **Constraints:** `unique(vendor_id, report_date)`, `check (porsi >= 0)`.
- [ ] **Schema** – `schemas.py`
  - **Classes:** `DistributionCreate`, `DistributionRead`, `DistributionUpdate`.
- [ ] **Repository** – `repositories.py`
  - **Functions:** `create_report`, `get_report`, `list_reports_by_vendor`, `update_report`.
- [ ] **Service** – `services.py`
  - **Functions:** `submit_report` (validasi geospasial + enqueue AI task), `process_anomaly(report_id)` (worker hook), `mask_report_fields`.
- [ ] **Policy** – `policies.py`
  - **Function:** `can_view_report(user, report)` → OPA check untuk scope wilayah.
- [ ] **Task Documentation** – `README.md` menjelaskan alur: UI → Server Action → Service → Repo → OPA → RLS.

## 🔒 Constraints & Best Practices
- **Geospasial Validation:** gunakan fungsi PostGIS `ST_DWithin(geo_point, school_location, radius + tolerance)`; toleransi default 50 m, configurable via env `RADIUS_TOLERANCE_M=50`.
- **Anomaly Detection:** laporan dikirim ke queue Redis; worker `validate_documents` (akan dibuat di `backend/workers/validate_documents/`) memanggil model AI dan menyimpan `anomaly_score`.
- **Idempotency:** header `X‑Idempotency‑Key` harus diproses pada endpoint `POST /distribution`.
- **Rate‑limit:** middleware `rate_limit` membatasi `POST /distribution` menjadi 10 request per menit per vendor.
- **Testing:** buat test di `backend/app/tests/distribution/` yang mensimulasikan validasi GIS dan anomali.

## 📄 References
- `api-contract.yaml` → endpoint `/distribution`.
- `docs/DESIGN.md` – bagian *Geospatial & AI Guard*.
- `docs/DATA_GOVERNANCE.md` – kebijakan foto & timestamp.

---

**Instruksi Eksplisit:** Tidak ada file kode yang boleh dibuat sebelum semua checklist di atas diberi tanda selesai (`[x]`).
