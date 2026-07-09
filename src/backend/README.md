# SIGAP Backend

Backend API untuk SIGAP menggunakan **FastAPI**, **SQLAlchemy**, dan **PostgreSQL/PostGIS**.

## Struktur

```text
app/
├── api/v1/              # Router endpoint per modul
├── core/                # Config, security, dependency umum
├── db/                  # Session, Base, Alembic metadata
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
└── services/            # Business logic
```

## Menjalankan lokal

```bash
cd src/backend
PYTHONPATH=. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://localhost:8000/healthz
```

## Test

```bash
cd src/backend
PYTHONPATH=. python -m pytest tests
```

## Catatan desain penting

- NIK tidak boleh diekspos penuh di response publik; gunakan `mask_nik()`.
- Scope RBAC mendukung banyak wilayah (`value: string[]`).
- Laporan distribusi menyimpan `radius`, `latitude`, dan `longitude` untuk validasi geospatial.
- Pengaduan bisa dikaitkan ke `distribution_id` dan `tanggal_kejadian`.
- Semua mutasi penting wajib dicatat ke `audit_logs` saat implementasi service CRUD dibuat.
