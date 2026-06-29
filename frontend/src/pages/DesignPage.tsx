import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import CollateralSelector from "../components/CollateralSelector";
import ParameterPanel from "../components/ParameterPanel";
import { useAppContext } from "../context/AppContext";
import { fetchExampleDesigns } from "../lib/api";
import { createDefaultDesign, modelLabels, type CollateralModelId, type Design } from "../types";

function DesignPage() {
  const navigate = useNavigate();
  const { currentDesign, setCurrentDesign, setLastResult, setCompareResult } = useAppContext();
  const [examples, setExamples] = useState<Design[]>([]);
  const [loadingExamples, setLoadingExamples] = useState(true);

  useEffect(() => {
    let active = true;
    fetchExampleDesigns()
      .then((payload) => {
        if (active) {
          setExamples(payload);
        }
      })
      .catch(() => undefined)
      .finally(() => {
        if (active) {
          setLoadingExamples(false);
        }
      });

    return () => {
      active = false;
    };
  }, []);

  const handleModelSelect = (model: CollateralModelId) => {
    setCurrentDesign(createDefaultDesign(model));
  };

  return (
    <div className="grid gap-6">
      <section className="panel p-6">
        <div className="mb-6">
          <p className="eyebrow">1. Design</p>
          <h2 className="mt-3 text-3xl font-semibold text-slate-950">Configure the mechanism first.</h2>
          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
            Choose one of the three supported collateral models, then set only the explicit parameters used by the
            simulation engine.
          </p>
        </div>
        <CollateralSelector selectedModel={currentDesign.collateral_model} onSelect={handleModelSelect} />
      </section>

      <ParameterPanel title={modelLabels[currentDesign.collateral_model]} design={currentDesign} onChange={setCurrentDesign} />

      <section className="panel p-6">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h2 className="text-2xl font-semibold text-slate-950">Seeded Examples</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              Load a baseline design if you want a known starting point before stress testing.
            </p>
          </div>
          <button
            type="button"
            className="action-button"
            onClick={() => {
              setLastResult(null);
              setCompareResult(null);
              navigate("/stress");
            }}
          >
            Continue to stress test
          </button>
        </div>

        <div className="mt-6 grid gap-4 md:grid-cols-2">
          {loadingExamples ? (
            <div className="rounded-[1.5rem] border border-slate-200 bg-slate-50 p-5 text-sm text-slate-600">Loading examples…</div>
          ) : null}
          {examples.map((example) => (
            <button
              key={example.label}
              type="button"
              onClick={() => setCurrentDesign(example)}
              className="rounded-[1.5rem] border border-slate-200 bg-white p-5 text-left transition hover:border-slate-300 hover:bg-slate-50"
            >
              <p className="font-semibold text-slate-950">{example.label}</p>
              <p className="mt-2 text-sm text-slate-600">{modelLabels[example.collateral_model]}</p>
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}

export default DesignPage;
