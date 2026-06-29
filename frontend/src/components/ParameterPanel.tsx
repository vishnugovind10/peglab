import type { ChangeEvent } from "react";

import type { CollateralType, Design, OracleType } from "../types";

interface ParameterPanelProps {
  title: string;
  design: Design;
  onChange: (design: Design) => void;
}

const collateralTypeOptions: { value: CollateralType; label: string }[] = [
  { value: "fiat", label: "Fiat" },
  { value: "crypto_basket", label: "Crypto basket" },
  { value: "mixed", label: "Mixed" },
];

const oracleOptions: { value: OracleType; label: string }[] = [
  { value: "chainlink_sim", label: "Chainlink sim" },
  { value: "twap_sim", label: "TWAP sim" },
  { value: "internal_sim", label: "Internal sim" },
];

const fieldHelp: Record<string, string> = {
  reserve_ratio: "Starting collateralization. 1.45 means 145% collateral.",
  mint_cap_per_step: "Maximum supply expansion per step during normal conditions.",
  redemption_rate_limit: "Maximum redemptions processed per step.",
  oracle_delay_steps: "Lag between collateral moves and oracle recognition.",
  liquidation_threshold: "Coverage threshold that triggers forced deleveraging.",
  fee_bps: "Mint and redemption fee in basis points.",
};

function updateNumberField(design: Design, key: keyof Design["config"], value: number): Design {
  return {
    ...design,
    config: {
      ...design.config,
      [key]: value,
    },
  };
}

function ParameterPanel({ title, design, onChange }: ParameterPanelProps) {
  const showCollateralBufferFields = design.collateral_model !== "fiat_backed";

  const handleLabelChange = (event: ChangeEvent<HTMLInputElement>) => {
    onChange({ ...design, label: event.target.value });
  };

  const handleNumberChange = (key: keyof Design["config"], roundToInt = false) => (event: ChangeEvent<HTMLInputElement>) => {
    const value = roundToInt ? Math.round(Number(event.target.value)) : Number(event.target.value);
    onChange(updateNumberField(design, key, value));
  };

  return (
    <section className="panel p-6">
      <div className="mb-6 flex items-center justify-between gap-3">
        <div>
          <h2 className="text-2xl font-semibold text-slate-950">{title}</h2>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Parameters stay explicit here so the simulation outputs remain auditable.
          </p>
        </div>
      </div>

      <div className="grid gap-5 md:grid-cols-2">
        <label className="md:col-span-2">
          <span className="field-label">Design Label</span>
          <input className="field-input mt-2" value={design.label ?? ""} onChange={handleLabelChange} />
        </label>

        {showCollateralBufferFields ? (
          <label>
            <span className="field-label">Reserve Ratio</span>
            <input
              className="field-input mt-2"
              type="number"
              step="0.01"
              min="1"
              max="5"
              value={design.config.reserve_ratio}
              onChange={handleNumberChange("reserve_ratio")}
            />
            <span className="field-help">{fieldHelp.reserve_ratio}</span>
          </label>
        ) : null}

        <label>
          <span className="field-label">Collateral Type</span>
          <select
            className="field-select mt-2"
            value={design.config.collateral_type}
            onChange={(event) =>
              onChange({
                ...design,
                config: { ...design.config, collateral_type: event.target.value as CollateralType },
              })
            }
          >
            {collateralTypeOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>

        <label>
          <span className="field-label">Mint Cap Per Step</span>
          <input
            className="field-input mt-2"
            type="number"
            step="0.1"
            min="0.1"
            max="50"
            value={design.config.mint_cap_per_step}
            onChange={handleNumberChange("mint_cap_per_step")}
          />
          <span className="field-help">{fieldHelp.mint_cap_per_step}</span>
        </label>

        <label>
          <span className="field-label">Redemption Rate Limit</span>
          <input
            className="field-input mt-2"
            type="number"
            step="0.1"
            min="0.1"
            max="50"
            value={design.config.redemption_rate_limit}
            onChange={handleNumberChange("redemption_rate_limit")}
          />
          <span className="field-help">{fieldHelp.redemption_rate_limit}</span>
        </label>

        <label>
          <span className="field-label">Oracle Type</span>
          <select
            className="field-select mt-2"
            value={design.config.oracle_type}
            onChange={(event) =>
              onChange({
                ...design,
                config: { ...design.config, oracle_type: event.target.value as OracleType },
              })
            }
          >
            {oracleOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>

        <label>
          <span className="field-label">Oracle Delay Steps</span>
          <input
            className="field-input mt-2"
            type="number"
            step="1"
            min="0"
            max="25"
            value={design.config.oracle_delay_steps}
            onChange={handleNumberChange("oracle_delay_steps", true)}
          />
          <span className="field-help">{fieldHelp.oracle_delay_steps}</span>
        </label>

        {showCollateralBufferFields ? (
          <label>
            <span className="field-label">Liquidation Threshold</span>
            <input
              className="field-input mt-2"
              type="number"
              step="0.01"
              min="0.8"
              max="3"
              value={design.config.liquidation_threshold}
              onChange={handleNumberChange("liquidation_threshold")}
            />
            <span className="field-help">{fieldHelp.liquidation_threshold}</span>
          </label>
        ) : null}

        <label>
          <span className="field-label">Fee (bps)</span>
          <input
            className="field-input mt-2"
            type="number"
            step="1"
            min="0"
            max="1000"
            value={design.config.fee_bps}
            onChange={handleNumberChange("fee_bps", true)}
          />
          <span className="field-help">{fieldHelp.fee_bps}</span>
        </label>
      </div>
    </section>
  );
}

export default ParameterPanel;
