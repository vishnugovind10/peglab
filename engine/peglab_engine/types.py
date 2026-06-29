from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal

FailureProbability = Literal["low", "medium", "high"]
CollateralType = Literal["fiat", "crypto_basket", "mixed"]
OracleType = Literal["chainlink_sim", "twap_sim", "internal_sim"]
CollateralModelId = Literal["fiat_backed", "crypto_backed", "overcollateralized"]


@dataclass(slots=True)
class CollateralConfig:
    reserve_ratio: float = 1.0
    collateral_type: CollateralType = "fiat"
    mint_cap_per_step: float = 4.0
    redemption_rate_limit: float = 8.0
    oracle_type: OracleType = "chainlink_sim"
    oracle_delay_steps: int = 0
    liquidation_threshold: float = 1.1
    fee_bps: int = 10


@dataclass(slots=True)
class DesignConfig:
    collateral_model: CollateralModelId
    config: CollateralConfig
    label: str | None = None


@dataclass(slots=True)
class ScenarioParameterDefinition:
    id: str
    label: str
    type: Literal["int", "float"]
    minimum: float
    maximum: float
    step: float
    default: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "type": self.type,
            "min": self.minimum,
            "max": self.maximum,
            "step": self.step,
            "default": self.default,
        }


@dataclass(slots=True)
class ScenarioShock:
    redemption_multiplier: float = 1.0
    redemption_spike: float = 0.0
    collateral_price_multiplier: float = 1.0
    slippage_multiplier: float = 1.0
    reserve_access_pct: float = 1.0
    oracle_frozen: bool = False
    interest_rate_delta_bps: int = 0
    governance_blocked: bool = False
    demand_multiplier: float = 1.0


@dataclass(slots=True)
class SimState:
    step: int
    peg_price: float
    collateral_ratio: float
    reserves: float
    mint_volume: float
    redeem_volume: float
    liquidation_volume: float
    supply: float
    reserve_units: float
    queue_pressure: float
    collateral_price: float
    oracle_price: float
    accessible_reserves_pct: float


@dataclass(slots=True)
class TimeseriesData:
    steps: list[int] = field(default_factory=list)
    peg_price: list[float] = field(default_factory=list)
    collateral_ratio: list[float] = field(default_factory=list)
    reserves: list[float] = field(default_factory=list)
    mint_volume: list[float] = field(default_factory=list)
    redeem_volume: list[float] = field(default_factory=list)
    liquidation_volume: list[float] = field(default_factory=list)
    supply: list[float] = field(default_factory=list)

    def append(self, state: SimState) -> None:
        self.steps.append(state.step)
        self.peg_price.append(round(state.peg_price, 6))
        self.collateral_ratio.append(round(state.collateral_ratio, 6))
        self.reserves.append(round(state.reserves, 6))
        self.mint_volume.append(round(state.mint_volume, 6))
        self.redeem_volume.append(round(state.redeem_volume, 6))
        self.liquidation_volume.append(round(state.liquidation_volume, 6))
        self.supply.append(round(state.supply, 6))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class SimulationResult:
    peg_stability_pct: float
    recovery_time_steps: int | None
    worst_drawdown_pct: float
    final_collateral_ratio: float
    failure_probability: FailureProbability
    recommendations: list[str]
    timeseries: TimeseriesData
    assumptions: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "peg_stability_pct": self.peg_stability_pct,
            "recovery_time_steps": self.recovery_time_steps,
            "worst_drawdown_pct": self.worst_drawdown_pct,
            "final_collateral_ratio": self.final_collateral_ratio,
            "failure_probability": self.failure_probability,
            "recommendations": self.recommendations,
            "timeseries": self.timeseries.to_dict(),
            "assumptions": self.assumptions,
        }
