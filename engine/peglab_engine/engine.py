from __future__ import annotations

from peglab_engine.assumptions import build_assumptions
from peglab_engine.metrics import build_simulation_result
from peglab_engine.models import MODEL_REGISTRY
from peglab_engine.scenarios import build_scenario
from peglab_engine.types import CollateralConfig, DesignConfig, SimulationResult


class SimulationEngine:
    def run(
        self,
        design: DesignConfig,
        scenario_id: str,
        scenario_params: dict[str, float | int] | None = None,
        num_steps: int = 100,
    ) -> SimulationResult:
        model_class = MODEL_REGISTRY.get(design.collateral_model)
        if model_class is None:
            raise KeyError(f"Unknown collateral model: {design.collateral_model}")

        scenario = build_scenario(scenario_id, scenario_params)
        model = model_class(design.config)
        state = model.initial_state()
        states = []

        for step in range(num_steps):
            shock = scenario.shock_for_step(step, num_steps)
            state = model.step(state, shock)
            states.append(state)

        assumptions = build_assumptions(design.collateral_model, scenario_id)
        return build_simulation_result(states, assumptions)


def run_simulation(
    collateral_model: str,
    config: CollateralConfig,
    scenario_id: str,
    scenario_params: dict[str, float | int] | None = None,
    num_steps: int = 100,
) -> SimulationResult:
    design = DesignConfig(collateral_model=collateral_model, config=config)
    return SimulationEngine().run(design, scenario_id, scenario_params, num_steps)
