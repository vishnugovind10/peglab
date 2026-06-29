from __future__ import annotations

from peglab_engine.scenarios.base import Scenario, within_window
from peglab_engine.types import ScenarioParameterDefinition, ScenarioShock


class BridgeFailureScenario(Scenario):
    id = "bridge_failure"
    name = "Bridge Failure"
    description = "Some collateral becomes inaccessible for a temporary window."
    parameter_schema = [
        ScenarioParameterDefinition("affected_pct", "Affected Percent", "float", 10.0, 90.0, 1.0, 35.0),
        ScenarioParameterDefinition("duration_steps", "Duration Steps", "int", 3, 40, 1, 12),
    ]

    def shock_for_step(self, step: int, num_steps: int) -> ScenarioShock:
        active = within_window(step, 15, int(self.params["duration_steps"]))
        reserve_access_pct = 1.0 - float(self.params["affected_pct"]) / 100 if active else 1.0
        return ScenarioShock(
            reserve_access_pct=max(0.1, reserve_access_pct),
            redemption_multiplier=1.2 if active else 1.0,
        )
