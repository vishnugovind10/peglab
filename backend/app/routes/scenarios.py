from __future__ import annotations

from fastapi import APIRouter
from peglab_engine import list_scenarios

from app.schemas import ScenarioMetadataSchema

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


@router.get("", response_model=list[ScenarioMetadataSchema])
def get_scenarios() -> list[dict[str, object]]:
    return list_scenarios()
