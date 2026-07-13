# TASK.md – Backend/policies

## Goals
- Menyimpan **OPA/CASL policy files** (`*.rego` atau `*.casl`) yang mengatur **ABAC** untuk semua resource.
- Pastikan policy dapat **dinamis di‑load** pada runtime dan di‑cache untuk performa.
- Sertakan **policy testing** (`opa test`) sebagai bagian dari CI.

## Verification Criteria
- [] File policy (`policy.rego`) ada dan valid (no syntax error).
- [] `opa eval` dapat men‑evaluate contoh request dan mengembalikan `allow = true/false` sesuai role.
- [] CI workflow menjalankan `opa test` dan gagal bila ada rule yang tidak tercover.
- [] Dokumentasi policy (`docs/POLICIES.md`) menjelaskan tiap rule dan contoh request.

## Status
- [ ] Pending
