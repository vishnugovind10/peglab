from __future__ import annotations

import json
from pathlib import Path

from peglab_engine import CollateralConfig, DesignConfig, SimulationEngine

from app.schemas import DesignSchema

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLES_DIR = REPO_ROOT / "examples"


def get_engine() -> SimulationEngine:
    return SimulationEngine()


def schema_to_design(design: DesignSchema) -> DesignConfig:
    return DesignConfig(
        collateral_model=design.collateral_model,
        label=design.label,
        config=CollateralConfig(**design.config.model_dump()),
    )


def load_example_designs() -> list[dict[str, object]]:
    configs = []
    for path in sorted(EXAMPLES_DIR.glob("*_config.json")):
        configs.append(json.loads(path.read_text(encoding="utf-8")))
    return configs
