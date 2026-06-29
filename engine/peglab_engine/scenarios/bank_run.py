from __future__ import annotations

from peglab_engine.scenarios.base import Scenario, within_window
from peglab_engine.types import ScenarioParameterDefinition, ScenarioShock


class BankRunScenario(Scenario):
    id = "bank_run"
    name = "Bank Run"
    description = "Sustained elevated redemptions stress reserve throughput."
    parameter_schema = [
        ScenarioParameterDefinition("redemption_multiplier", "Redemption Multiplier", "float", 1.5, 6.0, 0.1, 3.0),
        ScenarioParameterDefinition("duration_steps", "Duration Steps", "int", 5, 60, 1, 20),
    ]

    def shock_for_step(self, step: int, num_steps: int) -> ScenarioShock:
        active = within_window(step, 5, int(self.params["duration_steps"]))
        return ScenarioShock(redemption_multiplier=float(self.params["redemption_multiplier"]) if active else 1.0)
