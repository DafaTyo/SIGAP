# TASK.md – Backend/tests/middleware

## Goals
- Verify setiap middleware berfungsi sebagaimana mestinya dan tidak menambah latency signifikan.
- Simulasi request dengan/tanpa token, dengan/ tanpa izin OPA, dan cek audit log entry.

## Verification Criteria
- [] `CORS` header (`Access-Control-Allow-Origin`) muncul sesuai env config.
- [] `GZip` response ter‑compress untuk payload > 500 KB.
- [] `SecurityHeaders` hadir (`X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`).
- [] `RequestID` header `X-Request-ID` ter‑generate dan unik per request.
- [] `OPAEnforcement` meng‑return **403** bila policy deny.
- [] `AuditLogging` menulis entry ke tabel `vendor_audit` (verify via DB query).
- [] Total latency tambahan < 2 ms (measured dengan `time.perf_counter`).
- [] Coverage ≥ 90 % pada folder `middleware`.

## Status
- [ ] Pending
