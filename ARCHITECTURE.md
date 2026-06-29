# PegLab Architecture

```text
Frontend (React + TypeScript + Recharts)
  - Design configurator
  - Stress test runner
  - Results dashboard
  - Compare view
            |
            | JSON over HTTP
            v
Backend (FastAPI)
  - GET  /scenarios
  - GET  /designs/examples
  - POST /simulate
  - POST /compare
            |
            v
Simulation Engine (Pure Python)
  - collateral models
  - fixed stress scenarios
  - simulation loop
  - rule-based metrics
```

## Design Principles

- The engine is pure Python and has no FastAPI or frontend dependency.
- The backend is stateless per request.
- Saved designs live in browser `localStorage`.
- Assumptions are always returned with results and always rendered in the UI.

## Repository Layers

- `engine/` contains the testable simulation core.
- `backend/` validates requests and exposes the engine over HTTP.
- `frontend/` implements the four-page user flow and local persistence.
