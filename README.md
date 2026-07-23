# SIGAP Backend

Sistem Informasi Governance Aksi Pangan — backend API FastAPI modular monolith.

## Prasyarat

| Komponen | Cek |
|---|---|
| **Python 3.11+** | `python3 --version` / `python --version` |
| **uv** | `uv --version` |
| **Redis** | `redis-cli ping` → `PONG` |
| **PostgreSQL** (opsional, dev pake SQLite) | `psql --version` |
| **OPA** (opsional, skip aja) | — |

## Cara Running (WSL) ✅ Paling Stabil

```bash
# 1. Masuk WSL
wsl

# 2. Masuk folder proyek + aktifkan venv
cd /mnt/c/SIGAP
source .venv/bin/activate

# 3. Cek Redis
redis-cli ping
# → PONG

# 4. Jalanin server
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Akses dari browser Windows:**
- `http://localhost:8000/docs` — Swagger UI
- `http://localhost:8000/redoc` — Redoc
- `http://localhost:8000/health` — Health check

> **Catatan:** Server berjalan di port 8000. Kalau bentrok, ganti `--port 8001`.

---

## Cara Running (Windows — tanpa Redis)

```powershell
# PowerShell
cd C:\SIGAP
.venv\Scripts\activate

# Set env
$env:JWT_SECRET_KEY="dummy-...tion"
$env:NIK_ENCRYPTION_KEY="dummy-nik-encryption-key-16-bytes!!"

cd backend
uv run -- uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Test Endpoint

```bash
# Health check
curl http://localhost:8000/health

# Login
curl -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@sigap.gov&password=admin123"

# List vendor (ganti *** dengan token dari login)
curl http://localhost:8000/v1/vendors?page=1&page_size=10 \
  -H "Authorization: Bearer ***"
```

---

## Perintah Penting Lainnya

| Perintah | Fungsi |
|---|---|
| `uv sync` | Install/update dependencies |
| `uv pip install <package>` | Install package ke venv |
| `python -m pytest -v` | Jalanin test |
| `redis-cli ping` | Cek Redis |
| `psql -U user -d sigap` | Connect PostgreSQL |
| `alembic upgrade head` | Jalanin migrasi (PSQL) |
| `Ctrl + C` | Stop server |

---

## Troubleshooting

| Error | Solusi |
|---|---|
| `ModuleNotFoundError: No module named 'app'` | Pastikan `cd backend` dulu sebelum `python -m uvicorn ...` |
| `aiosqlite not found` | `uv pip install aiosqlite` |
| `email-validator not found` | `uv pip install email-validator` |
| `structlog` error | `uv pip install "structlog>=24.1.0,<25"` |
| `Port already in use` | Ganti port: `--port 8001` |
| `JWT_SECRET_KEY required` | Set env var `JWT_SECRET_KEY=...` (atau `.env` file) |
| Server start tapi `localhost:8000` gak kebuka | Pake `localhost`, **bukan** `0.0.0.0` di browser |
