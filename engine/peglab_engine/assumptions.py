from __future__ import annotations

MODEL_ASSUMPTIONS = {
    "fiat_backed": [
        "Fiat-backed designs assume reserve assets remain nominally stable at par.",
        "Redemptions are constrained by explicit rate limits and reserve accessibility rather than liquidation logic.",
    ],
    "crypto_backed": [
        "Crypto-backed designs mark reserve value to a simulated collateral price path every step.",
        "Liquidations are simplified threshold events and do not model auction microstructure.",
    ],
    "overcollateralized": [
        "Overcollateralized designs use the same crypto reserve mechanics with a larger starting collateral buffer.",
        "Higher buffers improve confidence but tie up more reserves in the model.",
    ],
}

SCENARIO_ASSUMPTIONS = {
    "bank_run": [
        "Bank-run shocks increase redemptions for a fixed duration with no behavioral adaptation.",
    ],
    "whale_redemption": [
        "Whale-redemption shocks model one outsized redemption at a single trigger step.",
    ],
    "oracle_failure": [
        "Oracle-failure shocks freeze oracle updates; no fallback oracle network is simulated.",
    ],
    "collateral_crash": [
        "Collateral-crash shocks apply a deterministic drawdown over a fixed number of steps.",
    ],
    "liquidity_crunch": [
        "Liquidity-crunch shocks amplify slippage rather than modeling order-book depth directly.",
    ],
    "interest_rate_spike": [
        "Interest-rate shocks affect confidence and demand rather than reserve yields line by line.",
    ],
    "bridge_failure": [
        "Bridge-failure shocks temporarily reduce the portion of collateral that can be accessed.",
    ],
    "governance_failure": [
        "Governance-failure shocks delay parameter responses during the active stress window.",
    ],
    "liquidity_mining_ends": [
        "Liquidity-mining-end shocks reduce demand abruptly with no secondary incentive response.",
    ],
    "black_swan": [
        "Black-swan shocks combine a collateral crash with a concurrent redemption wave.",
    ],
}

GLOBAL_ASSUMPTIONS = [
    "Shock timing is deterministic and exogenous to the system under test.",
    "The simulation does not model real market microstructure, live oracle feeds, or cross-venue arbitrage.",
]


def build_assumptions(model_id: str, scenario_id: str) -> list[str]:
    return GLOBAL_ASSUMPTIONS + MODEL_ASSUMPTIONS[model_id] + SCENARIO_ASSUMPTIONS[scenario_id]
