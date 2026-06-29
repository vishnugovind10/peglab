import { modelLabels, type CollateralModelId } from "../types";

const modelDescriptions: Record<CollateralModelId, string> = {
  fiat_backed: "1:1 reserve assumptions with redemption queues as the main fragility surface.",
  crypto_backed: "Floating collateral value with liquidation thresholds and oracle lag sensitivity.",
  overcollateralized: "Crypto-backed with a thicker reserve buffer for resilience and recovery tradeoffs.",
};

interface CollateralSelectorProps {
  selectedModel: CollateralModelId;
  onSelect: (model: CollateralModelId) => void;
}

function CollateralSelector({ selectedModel, onSelect }: CollateralSelectorProps) {
  return (
    <div className="grid gap-4 lg:grid-cols-3">
      {(Object.keys(modelLabels) as CollateralModelId[]).map((model) => {
        const active = model === selectedModel;
        return (
          <button
            key={model}
            type="button"
            onClick={() => onSelect(model)}
            className={`rounded-[1.5rem] border p-5 text-left transition ${
              active
                ? "border-amber-300 bg-amber-50 shadow-[0_18px_40px_rgba(245,158,11,0.18)]"
                : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50"
            }`}
          >
            <p className="font-semibold text-slate-950">{modelLabels[model]}</p>
            <p className="mt-3 text-sm leading-6 text-slate-600">{modelDescriptions[model]}</p>
          </button>
        );
      })}
    </div>
  );
}

export default CollateralSelector;
