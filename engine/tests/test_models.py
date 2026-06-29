from peglab_engine.models.crypto_backed import CryptoBackedModel
from peglab_engine.models.fiat_backed import FiatBackedModel
from peglab_engine.models.overcollateralized import OvercollateralizedModel
from peglab_engine.types import CollateralConfig, ScenarioShock


def test_fiat_backed_model_maintains_non_negative_reserves():
    model = FiatBackedModel(CollateralConfig())
    next_state = model.step(model.initial_state(), ScenarioShock(redemption_multiplier=3.0))
    assert next_state.reserves >= 0
    assert next_state.supply >= 1.0


def test_crypto_backed_model_reacts_to_collateral_drop():
    model = CryptoBackedModel(CollateralConfig(reserve_ratio=1.5))
    next_state = model.step(model.initial_state(), ScenarioShock(collateral_price_multiplier=0.85))
    assert next_state.collateral_ratio < 1.5


def test_overcollateralized_model_starts_with_buffer():
    model = OvercollateralizedModel(CollateralConfig(reserve_ratio=1.4))
    state = model.initial_state()
    assert state.collateral_ratio >= 1.4
