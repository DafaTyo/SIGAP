# TASK‑BE‑011‑01 – RLS Policy Definition & Migration

## Goals
- Definisikan kebijakan **Row‑Level Security (RLS)** untuk tabel utama (`vendors`, `distributions`, `complaints`).
- Buat skrip migrasi Alembic yang men‑aktifkan RLS dan men‑tambah policy `policy_vendor_scope`, `policy_distribution_scope`, `policy_complaint_scope`.
- Pastikan setiap koneksi FastAPI men‑set variabel session `app.current_user_id` dan `app.current_scope` (province/kota) sebelum query dijalankan.

## Verification Criteria
- [] Alembic migration `versions/xxxx_rls_policies.py` berhasil dijalankan (`alembic upgrade head`).
- [] Query biasa (`SELECT * FROM vendors`) **hanya** mengembalikan baris yang `scope_id` sesuai dengan `app.current_scope`.
- [] Unit test `tests/policies/test_rls.py` mem‑mock session variable dan meng‑assert bahwa data dari wilayah lain **tidak** terlihat.
- [] CI pipeline menjalankan migration test dan gagal bila policy tidak ter‑apply.

## Status
- [] Pending