from __future__ import annotations

from fastapi import APIRouter

from app.deps import load_example_designs
from app.schemas import DesignSchema

router = APIRouter(prefix="/designs", tags=["designs"])


@router.get("/examples", response_model=list[DesignSchema])
def get_example_designs() -> list[dict[str, object]]:
    return load_example_designs()
