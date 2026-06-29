import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
EXAMPLES_DIR = Path(__file__).resolve().parents[2] / "examples"


def load_design(name: str) -> dict[str, object]:
    return json.loads((EXAMPLES_DIR / name).read_text(encoding="utf-8"))


SCENARIO_IDS = [
    "bank_run",
    "whale_redemption",
    "oracle_failure",
    "collateral_crash",
    "liquidity_crunch",
    "interest_rate_spike",
    "bridge_failure",
    "governance_failure",
    "liquidity_mining_ends",
    "black_swan",
]


@pytest.mark.parametrize("scenario_id", SCENARIO_IDS)
@pytest.mark.parametrize("example_name", ["usdc_style_config.json", "makerdao_style_config.json"])
def test_simulate_returns_valid_schema_for_example_designs(example_name: str, scenario_id: str):
    response = client.post(
        "/simulate",
        json={
            "design": load_design(example_name),
            "scenario": {"id": scenario_id, "params": {}},
            "num_steps": 100,
        },
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["assumptions"]
    assert payload["recommendations"]
    assert len(payload["timeseries"]["steps"]) == 100


@pytest.mark.parametrize("scenario_id", SCENARIO_IDS)
def test_compare_returns_results_for_both_example_designs(scenario_id: str):
    response = client.post(
        "/compare",
        json={
            "design_a": load_design("usdc_style_config.json"),
            "design_b": load_design("makerdao_style_config.json"),
            "scenario": {"id": scenario_id, "params": {}},
            "num_steps": 100,
        },
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["design_a_result"]["timeseries"]["steps"]
    assert payload["design_b_result"]["timeseries"]["steps"]


def test_examples_and_scenarios_are_exposed():
    examples_response = client.get("/designs/examples")
    scenarios_response = client.get("/scenarios")

    assert examples_response.status_code == 200
    assert len(examples_response.json()) == 2
    assert scenarios_response.status_code == 200
    assert len(scenarios_response.json()) == 10
