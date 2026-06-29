export type CollateralModelId = "fiat_backed" | "crypto_backed" | "overcollateralized";
export type CollateralType = "fiat" | "crypto_basket" | "mixed";
export type OracleType = "chainlink_sim" | "twap_sim" | "internal_sim";
export type FailureProbability = "low" | "medium" | "high";

export interface CollateralConfig {
  reserve_ratio: number;
  collateral_type: CollateralType;
  mint_cap_per_step: number;
  redemption_rate_limit: number;
  oracle_type: OracleType;
  oracle_delay_steps: number;
  liquidation_threshold: number;
  fee_bps: number;
}

export interface Design {
  collateral_model: CollateralModelId;
  config: CollateralConfig;
  label?: string | null;
}

export interface ScenarioParameter {
  id: string;
  label: string;
  type: "int" | "float";
  min: number;
  max: number;
  step: number;
  default: number;
}

export interface ScenarioMetadata {
  id: string;
  name: string;
  description: string;
  parameters: ScenarioParameter[];
  defaults: Record<string, number>;
}

export interface ScenarioSelection {
  id: string;
  params: Record<string, number>;
}

export interface TimeseriesData {
  steps: number[];
  peg_price: number[];
  collateral_ratio: number[];
  reserves: number[];
  mint_volume: number[];
  redeem_volume: number[];
  liquidation_volume: number[];
  supply: number[];
}

export interface SimulationResult {
  peg_stability_pct: number;
  recovery_time_steps: number | null;
  worst_drawdown_pct: number;
  final_collateral_ratio: number;
  failure_probability: FailureProbability;
  recommendations: string[];
  timeseries: TimeseriesData;
  assumptions: string[];
}

export interface CompareResponse {
  design_a_result: SimulationResult;
  design_b_result: SimulationResult;
}

export const modelLabels: Record<CollateralModelId, string> = {
  fiat_backed: "Fiat-backed",
  crypto_backed: "Crypto-backed",
  overcollateralized: "Overcollateralized",
};

export function createDefaultDesign(model: CollateralModelId = "fiat_backed"): Design {
  const base: Record<CollateralModelId, Design> = {
    fiat_backed: {
      collateral_model: "fiat_backed",
      label: "Fiat-backed design",
      config: {
        reserve_ratio: 1,
        collateral_type: "fiat",
        mint_cap_per_step: 4,
        redemption_rate_limit: 9,
        oracle_type: "internal_sim",
        oracle_delay_steps: 0,
        liquidation_threshold: 1,
        fee_bps: 5,
      },
    },
    crypto_backed: {
      collateral_model: "crypto_backed",
      label: "Crypto-backed design",
      config: {
        reserve_ratio: 1.45,
        collateral_type: "crypto_basket",
        mint_cap_per_step: 3.5,
        redemption_rate_limit: 8,
        oracle_type: "chainlink_sim",
        oracle_delay_steps: 2,
        liquidation_threshold: 1.18,
        fee_bps: 15,
      },
    },
    overcollateralized: {
      collateral_model: "overcollateralized",
      label: "Overcollateralized design",
      config: {
        reserve_ratio: 1.65,
        collateral_type: "mixed",
        mint_cap_per_step: 3,
        redemption_rate_limit: 7.5,
        oracle_type: "twap_sim",
        oracle_delay_steps: 3,
        liquidation_threshold: 1.24,
        fee_bps: 10,
      },
    },
  };

  return structuredClone(base[model]);
}
