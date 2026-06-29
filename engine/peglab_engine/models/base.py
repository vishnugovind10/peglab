from __future__ import annotations

from abc import ABC, abstractmethod

from peglab_engine.types import CollateralConfig, ScenarioShock, SimState


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


class CollateralModel(ABC):
    model_id: str

    def __init__(self, config: CollateralConfig):
        self.config = config

    @abstractmethod
    def step(self, state: SimState, shock: ScenarioShock) -> SimState:
        """Advance simulation by one step."""

    @abstractmethod
    def initial_state(self) -> SimState:
        """Return the initial simulation state."""

    def _base_redemption_target(self, state: SimState, shock: ScenarioShock, confidence_bias: float = 0.0) -> float:
        base_redemption = state.supply * (0.02 + max(0.0, 1.0 - state.peg_price) * 0.08)
        target = base_redemption * shock.redemption_multiplier + shock.redemption_spike + state.queue_pressure * 0.55
        return max(0.0, target - confidence_bias)

    def _base_mint_volume(self, state: SimState, shock: ScenarioShock, confidence_multiplier: float = 1.0) -> float:
        fee_drag = self.config.fee_bps / 10_000
        demand = state.supply * 0.012 * shock.demand_multiplier * confidence_multiplier
        penalty = state.supply * max(0.0, 1.0 - state.peg_price) * 0.04
        target = max(0.0, demand - penalty - fee_drag * state.supply * 0.1)
        return min(self.config.mint_cap_per_step, target)

    def _next_oracle_price(self, state: SimState, collateral_price: float, shock: ScenarioShock) -> float:
        if shock.oracle_frozen:
            return state.oracle_price
        delay = max(0, self.config.oracle_delay_steps)
        smoothing = 1 / (delay + 1)
        return state.oracle_price + (collateral_price - state.oracle_price) * smoothing
