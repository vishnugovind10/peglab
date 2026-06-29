from __future__ import annotations

from peglab_engine.models.crypto_backed import CryptoBackedModel
from peglab_engine.models.base import clamp
from peglab_engine.types import ScenarioShock, SimState


class OvercollateralizedModel(CryptoBackedModel):
    model_id = "overcollateralized"

    def initial_state(self) -> SimState:
        state = super().initial_state()
        target_ratio = max(self.config.reserve_ratio, 1.35)
        reserve_units = 100.0 * target_ratio
        state.reserve_units = reserve_units
        state.reserves = reserve_units
        state.collateral_ratio = target_ratio
        return state

    def step(self, state: SimState, shock: ScenarioShock) -> SimState:
        next_state = super().step(state, shock)
        confidence_bonus = max(0.0, next_state.collateral_ratio - 1.1) * 0.04
        next_state.peg_price = clamp(next_state.peg_price + confidence_bonus, 0.45, 1.08)
        next_state.queue_pressure = max(0.0, next_state.queue_pressure * 0.8)
        return next_state
