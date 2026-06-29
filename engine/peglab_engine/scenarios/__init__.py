from peglab_engine.scenarios.bank_run import BankRunScenario
from peglab_engine.scenarios.base import Scenario
from peglab_engine.scenarios.black_swan import BlackSwanScenario
from peglab_engine.scenarios.bridge_failure import BridgeFailureScenario
from peglab_engine.scenarios.collateral_crash import CollateralCrashScenario
from peglab_engine.scenarios.governance_failure import GovernanceFailureScenario
from peglab_engine.scenarios.interest_rate_spike import InterestRateSpikeScenario
from peglab_engine.scenarios.liquidity_crunch import LiquidityCrunchScenario
from peglab_engine.scenarios.liquidity_mining_ends import LiquidityMiningEndsScenario
from peglab_engine.scenarios.oracle_failure import OracleFailureScenario
from peglab_engine.scenarios.whale_redemption import WhaleRedemptionScenario

SCENARIO_REGISTRY: dict[str, type[Scenario]] = {
    BankRunScenario.id: BankRunScenario,
    WhaleRedemptionScenario.id: WhaleRedemptionScenario,
    OracleFailureScenario.id: OracleFailureScenario,
    CollateralCrashScenario.id: CollateralCrashScenario,
    LiquidityCrunchScenario.id: LiquidityCrunchScenario,
    InterestRateSpikeScenario.id: InterestRateSpikeScenario,
    BridgeFailureScenario.id: BridgeFailureScenario,
    GovernanceFailureScenario.id: GovernanceFailureScenario,
    LiquidityMiningEndsScenario.id: LiquidityMiningEndsScenario,
    BlackSwanScenario.id: BlackSwanScenario,
}


def build_scenario(scenario_id: str, params: dict[str, float | int] | None = None) -> Scenario:
    scenario_class = SCENARIO_REGISTRY.get(scenario_id)
    if scenario_class is None:
        raise KeyError(f"Unknown scenario: {scenario_id}")
    return scenario_class(params)


def list_scenarios() -> list[dict[str, object]]:
    return [scenario_class().metadata() for scenario_class in SCENARIO_REGISTRY.values()]
