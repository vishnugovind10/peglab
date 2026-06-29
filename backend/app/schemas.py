from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class CollateralConfigSchema(BaseModel):
    reserve_ratio: float = Field(..., ge=1.0, le=5.0)
    collateral_type: Literal["fiat", "crypto_basket", "mixed"]
    mint_cap_per_step: float = Field(..., ge=0.1, le=50.0)
    redemption_rate_limit: float = Field(..., ge=0.1, le=50.0)
    oracle_type: Literal["chainlink_sim", "twap_sim", "internal_sim"]
    oracle_delay_steps: int = Field(..., ge=0, le=25)
    liquidation_threshold: float = Field(..., ge=0.8, le=3.0)
    fee_bps: int = Field(..., ge=0, le=1000)


class DesignSchema(BaseModel):
    collateral_model: Literal["fiat_backed", "crypto_backed", "overcollateralized"]
    config: CollateralConfigSchema
    label: str | None = None


class ScenarioSchema(BaseModel):
    id: str
    params: dict[str, float | int] = Field(default_factory=dict)


class SimulationRequestSchema(BaseModel):
    design: DesignSchema
    scenario: ScenarioSchema
    num_steps: int = Field(default=100, ge=10, le=500)


class CompareRequestSchema(BaseModel):
    design_a: DesignSchema
    design_b: DesignSchema
    scenario: ScenarioSchema
    num_steps: int = Field(default=100, ge=10, le=500)


class ScenarioParameterSchema(BaseModel):
    id: str
    label: str
    type: Literal["int", "float"]
    min: float
    max: float
    step: float
    default: float


class ScenarioMetadataSchema(BaseModel):
    id: str
    name: str
    description: str
    parameters: list[ScenarioParameterSchema]
    defaults: dict[str, float | int]


class TimeseriesDataSchema(BaseModel):
    steps: list[int]
    peg_price: list[float]
    collateral_ratio: list[float]
    reserves: list[float]
    mint_volume: list[float]
    redeem_volume: list[float]
    liquidation_volume: list[float]
    supply: list[float]


class SimulationResultSchema(BaseModel):
    peg_stability_pct: float
    recovery_time_steps: int | None
    worst_drawdown_pct: float
    final_collateral_ratio: float
    failure_probability: Literal["low", "medium", "high"]
    recommendations: list[str]
    timeseries: TimeseriesDataSchema
    assumptions: list[str]


class CompareResponseSchema(BaseModel):
    design_a_result: SimulationResultSchema
    design_b_result: SimulationResultSchema
