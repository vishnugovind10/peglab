from __future__ import annotations

from peglab_engine.scenarios.base import Scenario
from peglab_engine.types import ScenarioParameterDefinition, ScenarioShock


class WhaleRedemptionScenario(Scenario):
    id = "whale_redemption"
    name = "Whale Redemption"
    description = "A single large redemption hits the system at one step."
    parameter_schema = [
        ScenarioParameterDefinition("redemption_size", "Redemption Size", "float", 5.0, 40.0, 0.5, 18.0),
        ScenarioParameterDefinition("trigger_step", "Trigger Step", "int", 1, 80, 1, 18),
    ]

    def shock_for_step(self, step: int, num_steps: int) -> ScenarioShock:
        if step == int(self.params["trigger_step"]):
            return ScenarioShock(redemption_spike=float(self.params["redemption_size"]))
        return ScenarioShock()
