from __future__ import annotations

from peglab_engine.scenarios.base import Scenario, within_window
from peglab_engine.types import ScenarioParameterDefinition, ScenarioShock


class CollateralCrashScenario(Scenario):
    id = "collateral_crash"
    name = "Collateral Crash"
    description = "Collateral value falls sharply over a defined shock window."
    parameter_schema = [
        ScenarioParameterDefinition("crash_pct", "Crash Percent", "float", 10.0, 80.0, 1.0, 40.0),
        ScenarioParameterDefinition("crash_speed_steps", "Crash Speed", "int", 1, 20, 1, 5),
    ]

    def shock_for_step(self, step: int, num_steps: int) -> ScenarioShock:
        crash_speed = max(1, int(self.params["crash_speed_steps"]))
        if within_window(step, 8, crash_speed):
            total_drop = float(self.params["crash_pct"]) / 100
            per_step_drop = total_drop / crash_speed
            return ScenarioShock(
                collateral_price_multiplier=max(0.2, 1.0 - per_step_drop),
                redemption_multiplier=1.2,
            )
        return ScenarioShock()
