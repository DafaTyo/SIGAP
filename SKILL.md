# SKILL.md - SIGAP Development SOPs
# Dokumen ini berisi Standar Operasional Prosedur (SOP) untuk tugas teknis rutin dalam ekosistem SIGAP.

## 1. Menambahkan Endpoint API Baru
**Trigger**: Kebutuhan fitur baru yang memerlukan komunikasi client-server.

### Langkah-langkah:
1.  **Kontrak**: Update `api-contract.yaml` (Definisikan Request/Response, Header, Security).
2.  **Database**: Buat migrasi SQL jika perlu (pastikan RLS diterapkan).
3.  **Backend**: Tambahkan logic di `app/modules/[domain]/`. Pastikan PII masking di-handle.
4.  **Security**: Update OPA/CASL policy.
5.  **BFF**: Buat Server Action di Next.js.
6.  **Verify**: Jalankan `pytest` dan validasi response dengan `swagger-cli`.

## 2. Implementasi Kebijakan RLS (Row Level Security)
**Trigger**: Perubahan skema tabel yang memerlukan isolasi data wilayah.

### Langkah-langkah:
1.  **Migration**: Tambahkan `ALTER TABLE ... ENABLE ROW LEVEL SECURITY;`.
2.  **Policy**: Buat policy (`CREATE POLICY ... USING (scope_id = current_setting('app.current_scope'))`).
3.  **Application**: Pastikan setiap sesi FastAPI menjalankan `SET LOCAL app.current_scope = '...'`.
4.  **Verification**: Uji dengan user yang berbeda scope (pastikan query error/kosong).

## 3. Penanganan Anomali AI (Probabilistik)
**Trigger**: Menambahkan logic deteksi anomali baru.

### Langkah-langkah:
1.  **Logic**: Update model/script di `app/workers/anomaly_engine.py`.
2.  **Schema**: Pastikan return value berupa JSON: `{score: float, confidence: float, flag: enum, detected: boolean}`.
3.  **Alert**: Jika `detected == True`, picu event ke `complaint` module.
4.  **Verification**: Jalankan unit test dengan dummy data (berbagai nilai skor).

## 4. Audit Trail Entry
**Trigger**: Setiap operasi data (POST, PATCH, DELETE).

### Langkah-langkah:
1.  Gunakan middleware `AuditMiddleware` di FastAPI.
2.  Pastikan payload `old_values` dan `new_values` terisi dengan benar.
3.  Jangan log PII sensitif secara mentah (jika ada, harus di-masking sebelum masuk ke `audit_logs`).
