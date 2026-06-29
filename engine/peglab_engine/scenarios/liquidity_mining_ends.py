from __future__ import annotations

from peglab_engine.scenarios.base import Scenario, within_window
from peglab_engine.types import ScenarioParameterDefinition, ScenarioShock


class LiquidityMiningEndsScenario(Scenario):
    id = "liquidity_mining_ends"
    name = "Liquidity Mining Ends"
    description = "Incentive-driven demand falls and peg support weakens."
    parameter_schema = [
        ScenarioParameterDefinition("demand_drop_pct", "Demand Drop Percent", "float", 5.0, 80.0, 1.0, 25.0),
    ]

    def shock_for_step(self, step: int, num_steps: int) -> ScenarioShock:
        active = within_window(step, 6, 30)
        demand_multiplier = 1.0 - float(self.params["demand_drop_pct"]) / 100 if active else 1.0
        return ScenarioShock(
            demand_multiplier=max(0.1, demand_multiplier),
            redemption_multiplier=1.08 if active else 1.0,
        )
