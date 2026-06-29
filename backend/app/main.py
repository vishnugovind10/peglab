from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.compare import router as compare_router
from app.routes.designs import router as designs_router
from app.routes.scenarios import router as scenarios_router
from app.routes.simulate import router as simulate_router

app = FastAPI(title="PegLab API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(designs_router)
app.include_router(scenarios_router)
app.include_router(simulate_router)
app.include_router(compare_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
