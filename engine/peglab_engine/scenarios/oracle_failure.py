from __future__ import annotations

from peglab_engine.scenarios.base import Scenario, within_window
from peglab_engine.types import ScenarioParameterDefinition, ScenarioShock


class OracleFailureScenario(Scenario):
    id = "oracle_failure"
    name = "Oracle Failure"
    description = "Oracle values freeze and lag the underlying collateral move."
    parameter_schema = [
        ScenarioParameterDefinition("freeze_duration_steps", "Freeze Duration", "int", 3, 40, 1, 12),
    ]

    def shock_for_step(self, step: int, num_steps: int) -> ScenarioShock:
        active = within_window(step, 10, int(self.params["freeze_duration_steps"]))
        return ScenarioShock(
            oracle_frozen=active,
            collateral_price_multiplier=0.992 if active else 1.0,
            redemption_multiplier=1.15 if active else 1.0,
        )
