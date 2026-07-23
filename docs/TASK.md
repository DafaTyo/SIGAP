# 📌 Module Task Tracker: Docs Reference Package

## 🎯 Core Objective & Responsibility
- Menjadi pusat dokumentasi arsitektur, kebijakan data, dan requirement produk SIGAP.
- Menyimpan PRD, DESIGN.md, DATA_GOVERNANCE.md, AGENTS.md, CLAUDE.md sebagai single source of truth.

## 📋 Development Checklist
- [x] **PRD** – `PRD_SIGAP.md` (v1.0) mendefinisikan FR dan NFR.
- [x] **Design** – `DESIGN.md` menjelaskan arsitektur modular monolith.
- [x] **Data Governance** – `DATA_GOVERNANCE.md` (v1.1) kebijakan PII, RLS, audit.
- [x] **AGENTS.md** – protocol AI assistant SIGAP.
- [x] **CLAUDE.md** – coding standards & build commands.
- [x] **Context** – `context/*.txt` (PDF submissions ringkasan).
- [ ] **SKILL.md** – panduan implementasi spesifik fitur.
- [ ] **TASK.md** – tracker ini.

## 🔒 Constraints & Best Practices
- Semua perubahan API wajib di‑reflect di `api-contract.yaml` dulu (AGENTS.md primary directive).
- Dokumentasi harus selalu sinkron dengan implementasi kode.
- Tidak ada PII asli atau data sensitif di dokumentasi publik.
- Semua keputusan arsitektur dicatat sebagai ADR di DESIGN.md.

## 📄 References
- `api-contract.yaml` – kontrak API utama.
- `../backend/app/**` – implementasi teknis yang harus patuh pada dokumen ini.
- `../CONTEXT_SUMMARY.md` – ringkasan konteks proyek.
