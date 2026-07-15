# 📌 Module Task Tracker: Utils Package (backend/app/utils)

## 🎯 Core Objective & Responsibility
- Menyediakan **helper functions** yang dapat dipakai lintas domain:
  - PII masking (`mask_nik`, `mask_email`)
  - Pagination utilities (`paginate(query, page, size)`)
  - Cryptographic helpers (hash, verify)
  - Logging wrapper (JSON‑structured logger).
- Semua utilitas harus **stateless** dan tidak memiliki ketergantungan pada framework FastAPI.

## 📋 Development Checklist
- [ ] **Package init** – `__init__.py` yang men‑export semua utilitas utama.
- [ ] **Masking utilities** – `masking.py`
  - Functions: `mask_nik(nik: str) -> str` (format `####-####-####-1234`), `mask_email(email: str) -> str`.
- [ ] **Pagination utility** – `pagination.py`
  - Function: `def paginate(query, page: int = 1, page_size: int = 20) -> dict` (returns `items`, `total`, `page`, `page_size`).
- [ ] **Crypto helpers** – `crypto.py`
  - Functions: `hash_password(pwd)`, `verify_password(pwd, hashed)`, `encrypt(data)`, `decrypt(token)`.
- [ ] **JSON Logger wrapper** – `logger.py`
  - Function: `def get_json_logger(name: str) -> logging.Logger` dengan formatter JSON.
- [ ] **Write Utils README** – contoh import (`from app.utils.masking import mask_nik`).

## 🔒 Constraints & Best Practices
- **No external state:** utils tidak membuka DB atau cache; hanya operasi pure.
- **Performance:** gunakan `re` compiled regex untuk masking.
- **Security:** encryption menggunakan `cryptography` library, kunci di‑load dari env `APP_ENCRYPTION_KEY`.
- **Testing:** Unit‑test tiap fungsi di `backend/app/tests/utils/` dengan pytest.

## 📄 References
- `docs/DATA_GOVERNANCE.md` – aturan masking NIK & email.
- `docs/DESIGN.md` – kebutuhan pagination pada list endpoint.

---

**Instruksi Eksplisit:** Implementasi kode di folder utils **tidak boleh** dilakukan sebelum semua checklist di atas di‑centang selesai.
