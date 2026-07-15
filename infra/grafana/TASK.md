# 📌 Module Task Tracker: Infra Grafana (infra/grafana)

## 🎯 Core Objective ,  Responsibility 
- Menyediakan **Grafana** dashboard untuk visualisasi metrik Prometheus yang dikumpulkan dari SIGAP.
- Menyediakan dashboard standar: *API health*, *DB latency*, *AI anomaly score*, *request rate per endpoint*.

## 📋 Development Checklist
- [ ] **Package init** – `README.md` menjelaskan cara login (admin/admin) dan import dashboard JSON.
- [ ] **Dashboard JSON** – `dashboard.json`
  - Panels: `HTTP request latency`, `Error rate (%)`, `Distribution Anomaly Score avg`, `Vendor registration per hour`.
  - Datasource: `Prometheus` (named `Prometheus` in Grafana).
- [ ] **Provisioning Config** – `provisioning/datasources.yaml`
  - Set datasource URL `http://prometheus:9090` dan default interval.
- [ ] **Write Grafana README** – langkah import dashboard, set datasource, dan configure alerts.

## 🔒 Constraints & Best Practices
- **Security:** jangan expose admin password; gunakan env `GF_SECURITY_ADMIN_PASSWORD` (set via Docker compose).
- **Versioning:** dashboard JSON harus di‑track di git; setiap perubahan beri semver.
- **Retention:** Grafana tidak menyimpan data, hanya men‑render dari Prometheus.

## 📄 References
- `infra/prometheus/TASK.md` – alert rules yang akan dipakai.
- `docs/DESIGN.md` – metric list.

---

**Instruksi Eksplisit:** Tidak menulis dashboard JSON atau provisioning YAML sebelum semua item di atas di‑centang selesai.
