# TASK‑BE‑011‑03 – Idempotency Middleware

## Goals
- Implement FastAPI middleware `IdempotencyMiddleware` yang memeriksa header `X-Idempotency-Key` pada setiap request **POST**, **PUT**, atau **DELETE**.
- Middleware menyimpan pasangan `(key, response_body, status_code)` dalam tabel `idempotency_keys` selama 24 jam.
- Jika request dengan key yang sama datang lagi, middleware mengembalikan response yang sudah disimpan (tanpa mengeksekusi handler).
- Menyertakan mekanisme cleanup (cron job) untuk menghapus key yang kadaluwarsa.

## Verification Criteria
- [] Header `X-Idempotency-Key` wajib ada pada request yang mengubah state; bila tidak ada, middleware mengembalikan **400 Bad Request**.
- [] Pada request pertama, handler dijalankan dan response disimpan di tabel.
- [] Pada request kedua dengan key yang sama, middleware mengembalikan response yang disimpan (status & body identik) tanpa memanggil handler (bisa diverifikasi dengan mock).
- [] Unit test `tests/middleware/test_idempotency.py` mencakup kedua skenario.
- [] CI menjalankan test tersebut dan gagal bila middleware tidak berfungsi dengan benar.

## Status
- [] Pending