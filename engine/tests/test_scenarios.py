from peglab_engine.scenarios import SCENARIO_REGISTRY, build_scenario, list_scenarios


def test_scenario_registry_exposes_all_v1_scenarios():
    assert len(SCENARIO_REGISTRY) == 10
    assert len(list_scenarios()) == 10


def test_bank_run_shock_activates_after_warmup():
    scenario = build_scenario("bank_run", {"redemption_multiplier": 3.5, "duration_steps": 12})
    early_shock = scenario.shock_for_step(2, 100)
    active_shock = scenario.shock_for_step(8, 100)
    assert early_shock.redemption_multiplier == 1.0
    assert active_shock.redemption_multiplier == 3.5
