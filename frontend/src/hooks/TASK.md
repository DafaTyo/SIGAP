# 📌 Module Task Tracker: Frontend Hooks (frontend/src/hooks)

## 🎯 Core Objective & Responsibility
- Custom React hooks untuk state management, API fetching, form handling, dan auth state.

## 📋 Development Checklist
- [ ] **useAuth** – user session, login, logout, permissions.
- [ ] **useVendors** – fetch vendors list, filter, pagination.
- [ ] **useDistributions** – fetch distributions, map data, anomaly flags.
- [ ] **useComplaints** – fetch complaints, severity, SLA tracking.
- [ ] **useForm** – reusable form state dan validation.
- [ ] **useGeolocation** – GPS coordinate capture.
- [ ] **useDebounce** – debounce input untuk search.
- [ ] **useLocalStorage** – persist state ke localStorage.

## 🔒 Constraints & Best Practices
- Semua hooks wajib cleanup (useEffect return function).
- Error handling yang konsisten di setiap hook.
- Loading states untuk setiap async operation.
- TypeScript types wajib di-export.

## 📄 References
- `frontend/src/actions/` – Server Actions yang di-fetch.
- `frontend/src/components/` – komponen yang mengkonsumsi hooks.
- React Documentation – hooks best practices.