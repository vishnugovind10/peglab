from __future__ import annotations

from peglab_engine.scenarios.base import Scenario, within_window
from peglab_engine.types import ScenarioParameterDefinition, ScenarioShock


class GovernanceFailureScenario(Scenario):
    id = "governance_failure"
    name = "Governance Failure"
    description = "Operational responses are delayed or blocked during the incident."
    parameter_schema = [
        ScenarioParameterDefinition("delay_steps", "Delay Steps", "int", 3, 40, 1, 15),
    ]

    def shock_for_step(self, step: int, num_steps: int) -> ScenarioShock:
        active = within_window(step, 10, int(self.params["delay_steps"]))
        return ScenarioShock(
            governance_blocked=active,
            redemption_multiplier=1.18 if active else 1.0,
            demand_multiplier=0.88 if active else 1.0,
        )
