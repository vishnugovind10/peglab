from __future__ import annotations

import argparse
import json
from pathlib import Path

from peglab_engine import CollateralConfig, DesignConfig, SimulationEngine


def load_design(path: Path) -> DesignConfig:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return DesignConfig(
        collateral_model=payload["collateral_model"],
        label=payload.get("label"),
        config=CollateralConfig(**payload["config"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a PegLab simulation without the web stack.")
    parser.add_argument("--config", required=True, help="Path to a design config JSON file.")
    parser.add_argument("--scenario", required=True, help="Scenario id to run.")
    parser.add_argument("--num-steps", type=int, default=100, help="Simulation length.")
    parser.add_argument(
        "--params",
        default="{}",
        help="JSON object with scenario parameters, for example '{\"duration_steps\": 10}'.",
    )
    args = parser.parse_args()

    design = load_design(Path(args.config))
    scenario_params = json.loads(args.params)
    result = SimulationEngine().run(design, args.scenario, scenario_params, args.num_steps)

    output = {
        "design": design.label or design.collateral_model,
        "scenario": args.scenario,
        "peg_stability_pct": result.peg_stability_pct,
        "recovery_time_steps": result.recovery_time_steps,
        "worst_drawdown_pct": result.worst_drawdown_pct,
        "final_collateral_ratio": result.final_collateral_ratio,
        "failure_probability": result.failure_probability,
        "recommendations": result.recommendations,
        "assumptions": result.assumptions,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
