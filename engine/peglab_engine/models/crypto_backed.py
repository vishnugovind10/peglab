from __future__ import annotations

from peglab_engine.models.base import CollateralModel, clamp
from peglab_engine.types import ScenarioShock, SimState


class CryptoBackedModel(CollateralModel):
    model_id = "crypto_backed"

    def initial_state(self) -> SimState:
        reserve_ratio = max(self.config.reserve_ratio, 1.05)
        reserve_units = 100.0 * reserve_ratio
        return SimState(
            step=0,
            peg_price=1.0,
            collateral_ratio=reserve_ratio,
            reserves=reserve_units,
            mint_volume=0.0,
            redeem_volume=0.0,
            liquidation_volume=0.0,
            supply=100.0,
            reserve_units=reserve_units,
            queue_pressure=0.0,
            collateral_price=1.0,
            oracle_price=1.0,
            accessible_reserves_pct=1.0,
        )

    def step(self, state: SimState, shock: ScenarioShock) -> SimState:
        collateral_price = max(0.2, state.collateral_price * shock.collateral_price_multiplier)
        oracle_price = max(0.2, self._next_oracle_price(state, collateral_price, shock))
        accessible_units = state.reserve_units * shock.reserve_access_pct
        accessible_reserves = accessible_units * oracle_price

        confidence_bias = max(0.0, (state.collateral_ratio - 1.0) * 2.5)
        redemption_target = self._base_redemption_target(state, shock, confidence_bias=confidence_bias)
        served_redemption = min(redemption_target, self.config.redemption_rate_limit, accessible_reserves)
        queue_pressure = max(0.0, redemption_target - served_redemption)

        confidence_multiplier = max(0.25, min(1.75, state.collateral_ratio))
        mint_volume = self._base_mint_volume(state, shock, confidence_multiplier=confidence_multiplier)
        mint_volume *= max(0.35, min(1.0, shock.reserve_access_pct + 0.1))
        mint_volume = min(self.config.mint_cap_per_step, mint_volume)

        redeem_units = served_redemption / max(oracle_price, 0.2)
        mint_units = mint_volume / max(oracle_price, 0.2)
        next_reserve_units = max(0.0, state.reserve_units + mint_units - redeem_units)
        next_supply = max(1.0, state.supply + mint_volume - served_redemption)

        market_collateral_ratio = next_reserve_units * collateral_price * shock.reserve_access_pct / next_supply
        liquidation_volume = 0.0
        if market_collateral_ratio < self.config.liquidation_threshold:
            liquidation_gap = self.config.liquidation_threshold - market_collateral_ratio
            liquidation_volume = min(
                next_supply * (0.015 + liquidation_gap * 0.12),
                next_reserve_units * collateral_price * 0.18,
            )
            if shock.governance_blocked:
                liquidation_volume *= 0.45

        if liquidation_volume > 0:
            liquidation_units = liquidation_volume / max(collateral_price, 0.2)
            next_reserve_units = max(0.0, next_reserve_units - liquidation_units)
            next_supply = max(1.0, next_supply - liquidation_volume)

        reserves = next_reserve_units * collateral_price * shock.reserve_access_pct
        collateral_ratio = reserves / next_supply

        queue_ratio = queue_pressure / max(next_supply, 1.0)
        collateral_shortfall = max(0.0, 1.0 - collateral_ratio)
        price_pressure = queue_ratio * 0.7
        price_pressure += (shock.slippage_multiplier - 1.0) * 0.05
        price_pressure += collateral_shortfall * 0.4
        price_pressure += max(0.0, 1.0 - collateral_price) * 0.2
        support = max(0.0, collateral_ratio - 1.0) * 0.08
        support += liquidation_volume / max(next_supply, 1.0) * 0.12
        peg_price = clamp(1.0 - price_pressure + support, 0.4, 1.08)

        return SimState(
            step=state.step + 1,
            peg_price=peg_price,
            collateral_ratio=collateral_ratio,
            reserves=reserves,
            mint_volume=mint_volume,
            redeem_volume=served_redemption,
            liquidation_volume=liquidation_volume,
            supply=next_supply,
            reserve_units=next_reserve_units,
            queue_pressure=queue_pressure,
            collateral_price=collateral_price,
            oracle_price=oracle_price,
            accessible_reserves_pct=shock.reserve_access_pct,
        )
