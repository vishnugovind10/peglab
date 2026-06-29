from __future__ import annotations

from peglab_engine.scenarios.base import Scenario, within_window
from peglab_engine.types import ScenarioParameterDefinition, ScenarioShock


class LiquidityCrunchScenario(Scenario):
    id = "liquidity_crunch"
    name = "Liquidity Crunch"
    description = "Market depth thins and redemption slippage rises."
    parameter_schema = [
        ScenarioParameterDefinition("slippage_multiplier", "Slippage Multiplier", "float", 1.1, 5.0, 0.1, 2.4),
    ]

    def shock_for_step(self, step: int, num_steps: int) -> ScenarioShock:
        active = within_window(step, 12, 18)
        return ScenarioShock(slippage_multiplier=float(self.params["slippage_multiplier"]) if active else 1.0)
