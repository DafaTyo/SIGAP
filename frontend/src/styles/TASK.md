# 📌 Module Task Tracker: Styles Package (frontend/src/styles)

## 🎯 Core Objective & Responsibility
- Menyimpan **style definitions** untuk proyek Next.js, termasuk Tailwind configuration, CSS‑Modules, dan design token file.
- Tidak mengandung kode JavaScript/TypeScript, hanya konfigurasi styling.

## 📋 Development Checklist
- [ ] **Package init** – `index.ts` (optional, hanya untuk re‑export jika diperlukan).
- [ ] **Tailwind Config** – `tailwind.config.js`
  - Define custom colors, spacing, typography based on `docs/DESIGN.md` palette.
  - Enable JIT mode, purge paths `./src/**/*.tsx`.
- [ ] **Design Tokens** – `tokens.css` (or `tokens.module.css`)
  - Variables: `--color-primary`, `--spacing-sm`, `--border-radius`, dll.
- [ ] **Global CSS** – `globals.css`
  - Import Tailwind base, components, utilities; set `html, body` font family.
- [ ] **Write Styles README** – pola penggunaan Tailwind vs CSS‑Modules, contoh `className={styles.buttonPrimary}`.

## 🔒 Constraints & Best Practices
- **No inline styles** in React components – always use Tailwind classes or CSS‑Modules.
- **Purge unused CSS** to keep bundle size < 150 KB.
- **Accessibility:** ensure high contrast colors, focus outlines.
- **Testing:** use `storybook` (optional) to visual‑test components.

## 📄 References
- `docs/DESIGN.md` – color palette, typography, spacing guidelines.
- `frontend/src/components/` – contoh penggunaan classNames.

---

**Instruksi Eksplisit:** Tidak ada file konfigurasi styling yang boleh di‑commit (Tailwind, CSS) sebelum checklist di atas ditandai selesai.
