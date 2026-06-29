from __future__ import annotations

from fastapi import APIRouter, Depends

from app.deps import get_engine, schema_to_design
from app.schemas import SimulationRequestSchema, SimulationResultSchema

router = APIRouter(prefix="/simulate", tags=["simulate"])


@router.post("", response_model=SimulationResultSchema)
def simulate(
    request: SimulationRequestSchema,
    engine=Depends(get_engine),
) -> dict[str, object]:
    result = engine.run(
        design=schema_to_design(request.design),
        scenario_id=request.scenario.id,
        scenario_params=request.scenario.params,
        num_steps=request.num_steps,
    )
    return result.to_dict()
