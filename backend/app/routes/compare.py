from __future__ import annotations

from fastapi import APIRouter, Depends

from app.deps import get_engine, schema_to_design
from app.schemas import CompareRequestSchema, CompareResponseSchema

router = APIRouter(prefix="/compare", tags=["compare"])


@router.post("", response_model=CompareResponseSchema)
def compare(
    request: CompareRequestSchema,
    engine=Depends(get_engine),
) -> dict[str, object]:
    scenario_id = request.scenario.id
    scenario_params = request.scenario.params

    design_a_result = engine.run(
        design=schema_to_design(request.design_a),
        scenario_id=scenario_id,
        scenario_params=scenario_params,
        num_steps=request.num_steps,
    )
    design_b_result = engine.run(
        design=schema_to_design(request.design_b),
        scenario_id=scenario_id,
        scenario_params=scenario_params,
        num_steps=request.num_steps,
    )
    return {
        "design_a_result": design_a_result.to_dict(),
        "design_b_result": design_b_result.to_dict(),
    }
