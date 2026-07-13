# TASK‑BE‑011‑02 – PII Masking Utility (BFF)

## Goals
- Buat utilitas di **Next.js BFF** (`frontend/src/utils/maskPii.ts`) yang men‑mask field sensitif (NIK, phone, email) berdasarkan role.
- Export fungsi `maskPii<T>(data: T, role: string): T` yang meng‑replace bagian tengah NIK menjadi `####-####-1234` untuk semua role selain `admin`.
- Pastikan utilitas dapat dipanggil di API routes serta di server‑side rendering (SSR) sebelum mengirimkan data ke client.

## Verification Criteria
- [] Fungsi `maskPii` meng‑embalikan objek dengan field NIK ter‑mask untuk role `viewer` dan tidak ter‑mask untuk role `admin`.
- [] Unit test `frontend/src/utils/__tests__/maskPii.test.ts` memverifikasi semua skenario masking.
- [] CI pipeline menjalankan test utilitas tersebut dan gagal bila masking tidak tepat.
- [] Dokumentasi di `README` BFF men‑jelaskan cara meng‑import dan menggunakan utilitas.

## Status
- [] Pending