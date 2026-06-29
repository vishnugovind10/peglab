from __future__ import annotations

from peglab_engine.scenarios.base import Scenario, within_window
from peglab_engine.types import ScenarioParameterDefinition, ScenarioShock


class BlackSwanScenario(Scenario):
    id = "black_swan"
    name = "Black Swan"
    description = "A collateral crash lands at the same time as a redemption wave."
    parameter_schema = [
        ScenarioParameterDefinition("crash_pct", "Crash Percent", "float", 15.0, 85.0, 1.0, 55.0),
        ScenarioParameterDefinition("crash_speed_steps", "Crash Speed", "int", 1, 12, 1, 4),
        ScenarioParameterDefinition("redemption_multiplier", "Redemption Multiplier", "float", 1.5, 8.0, 0.1, 3.8),
        ScenarioParameterDefinition("duration_steps", "Duration Steps", "int", 5, 40, 1, 18),
    ]

    def shock_for_step(self, step: int, num_steps: int) -> ScenarioShock:
        crash_speed = max(1, int(self.params["crash_speed_steps"]))
        total_drop = float(self.params["crash_pct"]) / 100
        per_step_drop = total_drop / crash_speed
        crash_active = within_window(step, 8, crash_speed)
        redemption_active = within_window(step, 8, int(self.params["duration_steps"]))
        return ScenarioShock(
            collateral_price_multiplier=max(0.18, 1.0 - per_step_drop) if crash_active else 1.0,
            redemption_multiplier=float(self.params["redemption_multiplier"]) if redemption_active else 1.0,
            slippage_multiplier=1.6 if redemption_active else 1.0,
        )
