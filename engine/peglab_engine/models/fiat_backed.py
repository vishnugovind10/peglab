from __future__ import annotations

from peglab_engine.models.base import CollateralModel, clamp
from peglab_engine.types import ScenarioShock, SimState


class FiatBackedModel(CollateralModel):
    model_id = "fiat_backed"

    def initial_state(self) -> SimState:
        initial_reserves = 100.0
        return SimState(
            step=0,
            peg_price=1.0,
            collateral_ratio=1.0,
            reserves=initial_reserves,
            mint_volume=0.0,
            redeem_volume=0.0,
            liquidation_volume=0.0,
            supply=100.0,
            reserve_units=initial_reserves,
            queue_pressure=0.0,
            collateral_price=1.0,
            oracle_price=1.0,
            accessible_reserves_pct=1.0,
        )

    def step(self, state: SimState, shock: ScenarioShock) -> SimState:
        accessible_reserves = state.reserves * shock.reserve_access_pct
        redemption_target = self._base_redemption_target(state, shock)
        served_redemption = min(redemption_target, self.config.redemption_rate_limit, accessible_reserves)
        queue_pressure = max(0.0, redemption_target - served_redemption)

        confidence_multiplier = 1.0 - max(0.0, 1.0 - shock.reserve_access_pct) * 0.7
        confidence_multiplier -= max(0.0, shock.interest_rate_delta_bps) / 20_000
        mint_volume = self._base_mint_volume(state, shock, max(0.2, confidence_multiplier))

        fee_rate = self.config.fee_bps / 10_000
        next_reserves = max(0.0, state.reserves + mint_volume * (1 - fee_rate) - served_redemption)
        next_supply = max(1.0, state.supply + mint_volume - served_redemption)
        collateral_ratio = next_reserves / next_supply

        queue_ratio = queue_pressure / max(next_supply, 1.0)
        reserve_shortfall = max(0.0, 1.0 - collateral_ratio)
        price_pressure = queue_ratio * 0.9 + (shock.slippage_multiplier - 1.0) * 0.06 + reserve_shortfall * 0.45
        support = max(0.0, collateral_ratio - 1.0) * 0.05 + mint_volume / next_supply * 0.2
        peg_price = clamp(1.0 - price_pressure + support, 0.55, 1.08)

        return SimState(
            step=state.step + 1,
            peg_price=peg_price,
            collateral_ratio=collateral_ratio,
            reserves=next_reserves,
            mint_volume=mint_volume,
            redeem_volume=served_redemption,
            liquidation_volume=0.0,
            supply=next_supply,
            reserve_units=next_reserves,
            queue_pressure=queue_pressure,
            collateral_price=1.0,
            oracle_price=1.0,
            accessible_reserves_pct=shock.reserve_access_pct,
        )
