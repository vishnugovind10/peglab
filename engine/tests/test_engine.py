import pytest

from peglab_engine.engine import SimulationEngine
from peglab_engine.scenarios import SCENARIO_REGISTRY
from peglab_engine.types import CollateralConfig, DesignConfig


MODEL_CONFIGS = {
    "fiat_backed": CollateralConfig(
        reserve_ratio=1.0,
        collateral_type="fiat",
        mint_cap_per_step=4.0,
        redemption_rate_limit=9.0,
        oracle_type="internal_sim",
        oracle_delay_steps=0,
        liquidation_threshold=1.0,
        fee_bps=5,
    ),
    "crypto_backed": CollateralConfig(
        reserve_ratio=1.45,
        collateral_type="crypto_basket",
        mint_cap_per_step=3.5,
        redemption_rate_limit=8.0,
        oracle_type="chainlink_sim",
        oracle_delay_steps=2,
        liquidation_threshold=1.18,
        fee_bps=15,
    ),
    "overcollateralized": CollateralConfig(
        reserve_ratio=1.65,
        collateral_type="mixed",
        mint_cap_per_step=3.0,
        redemption_rate_limit=7.5,
        oracle_type="twap_sim",
        oracle_delay_steps=3,
        liquidation_threshold=1.24,
        fee_bps=10,
    ),
}


@pytest.mark.parametrize("model_id", MODEL_CONFIGS)
@pytest.mark.parametrize("scenario_id", SCENARIO_REGISTRY)
def test_all_model_scenario_combinations_produce_results(model_id: str, scenario_id: str):
    engine = SimulationEngine()
    result = engine.run(
        DesignConfig(collateral_model=model_id, config=MODEL_CONFIGS[model_id]),
        scenario_id,
        num_steps=100,
    )

    assert result.assumptions
    assert result.recommendations
    assert len(result.timeseries.steps) == 100
    assert len(result.timeseries.peg_price) == 100
    assert result.failure_probability in {"low", "medium", "high"}
