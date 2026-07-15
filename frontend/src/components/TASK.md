# 📌 Module Task Tracker: Components Package (frontend/src/components)

## 🎯 Core Objective & Responsibility
- Menyimpan **komponen UI** yang bersifat presentational (tidak mengandung business logic). 
- Komponen dibuat dengan **React (TSX)**, memanfaatkan TailwindCSS atau CSS‑Modules.
- Semua komponen harus **stateless**; state dikelola melalui hooks atau server actions.

## 📋 Development Checklist
- [ ] **Package init** – `index.ts` yang men‑export semua komponen utama (Button, Card, Modal, Table).
- [ ] **Button Component** – `Button.tsx`
  - Props: `variant` (`primary`,`secondary`,`danger`), `onClick`, `type`, `disabled`, `children`.
  - Styles: Tailwind classes, accessible ARIA attributes.
- [ ] **Card Component** – `Card.tsx`
  - Props: `title`, `subtitle?`, `children`, optional `footer`.
- [ ] **Modal Component** – `Modal.tsx`
  - Props: `isOpen`, `onClose`, `title`, `children`.
- [ ] **Table Component** – `Table.tsx`
  - Props: `columns` (array of {header:string, accessor:string}), `data` (array of objects), optional `onRowClick`.
- [ ] **Write Component README** – menjelaskan konvensi penamaan, styling guide, dan contoh penggunaan di halaman.

## 🔒 Constraints & Best Practices
- **No direct API calls** – gunakan hooks atau server actions untuk fetch data.
- **Accessibility:** semua komponen harus memiliki proper ARIA labels, focus management.
- **Testing:** gunakan React Testing Library untuk unit test, pastikan snapshot testing untuk UI.
- **Styling:** gunakan utility‑first Tailwind; hindari inline styles kecuali diperlukan.

## 📄 References
- `docs/DESIGN.md` – UI component guidelines, color palette.
- `frontend/src/styles/` – design tokens (font, spacing, colors).

---

**Instruksi Eksplisit:** Kode komponen React **tidak boleh** ditulis sebelum semua checklist di atas dibubuhi tanda selesai.
