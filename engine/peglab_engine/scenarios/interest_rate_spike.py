from __future__ import annotations

from peglab_engine.scenarios.base import Scenario, within_window
from peglab_engine.types import ScenarioParameterDefinition, ScenarioShock


class InterestRateSpikeScenario(Scenario):
    id = "interest_rate_spike"
    name = "Interest Rate Spike"
    description = "A rate shock reduces confidence in reserve carry assumptions."
    parameter_schema = [
        ScenarioParameterDefinition("rate_delta_bps", "Rate Delta (bps)", "int", 50, 1200, 25, 300),
    ]

    def shock_for_step(self, step: int, num_steps: int) -> ScenarioShock:
        active = within_window(step, 10, 25)
        return ScenarioShock(
            interest_rate_delta_bps=int(self.params["rate_delta_bps"]) if active else 0,
            demand_multiplier=0.78 if active else 1.0,
            redemption_multiplier=1.15 if active else 1.0,
        )
