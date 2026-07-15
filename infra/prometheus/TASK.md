# 📌 Module Task Tracker: Infra Prometheus (infra/prometheus)

## 🎯 Core Objective & Responsibility
- Menyiapkan **Prometheus** untuk meng‑scrape metrik dari FastAPI backend (`/metrics`) dan dari Redis/OPA bila diperlukan.
- Menyediakan **alerting rules** dasar (up/down, high latency, error rate).

## 📋 Development Checklist
- [ ] **Package init** – `README.md` dengan petunjuk instalasi.
- [ ] **Prometheus Config** – `prometheus.yml`
  - Scrape `backend:8000/metrics` every 15s.
  - Optional: scrape `redis:6379` via `redis_exporter` (future).
  - Define job `sigap_backend`.
- [ ] **Alerting Rules** – `alerts.yml`
  - Alert if `up{job="sigap_backend"} == 0` for >1m.
  - Alert if `http_requests_total{status="5.."}` > 5 per minute.
- [ ] **Write Prometheus README** – cara menjalankan `prometheus --config.file=prometheus.yml` dan mengakses UI (`localhost:9090`).

## 🔒 Constraints & Best Practices
- **Retention:** keep 15 days of data (set in Prometheus args).
- **Security:** expose Prometheus only inside Docker network (`sigap_net`).
- **Metrics Naming:** follow `snake_case` convention, prefix `sigap_`.

## 📄 References
- `docs/DESIGN.md` – kebutuhan observability.
- `infra/docker/docker-compose.yml` – service definition.

---

**Instruksi Eksplisit:** Tidak menulis `prometheus.yml` atau `alerts.yml` sebelum checklist di atas ditandai selesai.
