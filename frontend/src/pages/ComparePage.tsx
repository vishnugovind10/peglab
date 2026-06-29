import { useEffect, useState } from "react";

import CompareTable from "../components/CompareTable";
import ParameterPanel from "../components/ParameterPanel";
import ScenarioPicker from "../components/ScenarioPicker";
import CollateralRatioChart from "../components/charts/CollateralRatioChart";
import PegPriceChart from "../components/charts/PegPriceChart";
import ReservesChart from "../components/charts/ReservesChart";
import SupplyFlowChart from "../components/charts/SupplyFlowChart";
import { useAppContext } from "../context/AppContext";
import { compareDesigns, fetchExampleDesigns, fetchScenarios } from "../lib/api";
import { createDefaultDesign, type Design, type ScenarioMetadata, type ScenarioSelection } from "../types";

function ComparePage() {
  const { currentDesign, currentScenario, compareResult, setCompareResult, setCurrentScenario } = useAppContext();
  const [designA, setDesignA] = useState<Design>(currentDesign);
  const [designB, setDesignB] = useState<Design>(createDefaultDesign("overcollateralized"));
  const [examples, setExamples] = useState<Design[]>([]);
  const [scenarios, setScenarios] = useState<ScenarioMetadata[]>([]);
  const [localScenario, setLocalScenario] = useState<ScenarioSelection | null>(currentScenario);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setDesignA(currentDesign);
  }, [currentDesign]);

  useEffect(() => {
    let active = true;
    Promise.all([fetchExampleDesigns(), fetchScenarios()])
      .then(([examplePayload, scenarioPayload]) => {
        if (!active) {
          return;
        }
        setExamples(examplePayload);
        setScenarios(scenarioPayload);
        const makerDaoExample = examplePayload.find((example) => example.collateral_model === "overcollateralized");
        if (makerDaoExample) {
          setDesignB(makerDaoExample);
        }
        if (!localScenario && scenarioPayload[0]) {
          const firstScenario = { id: scenarioPayload[0].id, params: { ...scenarioPayload[0].defaults } };
          setLocalScenario(firstScenario);
          setCurrentScenario(firstScenario);
        }
      })
      .catch((requestError: Error) => {
        if (active) {
          setError(requestError.message);
        }
      })
      .finally(() => {
        if (active) {
          setLoading(false);
        }
      });

    return () => {
      active = false;
    };
  }, [localScenario, setCurrentScenario]);

  const runComparison = async () => {
    if (!localScenario) {
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const result = await compareDesigns(designA, designB, localScenario);
      setCompareResult(result);
      setCurrentScenario(localScenario);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Comparison failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="grid gap-6">
      <section className="panel p-6">
        <p className="eyebrow">4. Compare</p>
        <h2 className="mt-3 text-3xl font-semibold text-slate-950">Run two designs against the same shock.</h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
          Design A starts from the last active configuration. Design B can be edited directly or loaded from an example.
        </p>
      </section>

      <div className="grid gap-6 xl:grid-cols-2">
        <ParameterPanel title="Design A" design={designA} onChange={setDesignA} />
        <div className="grid gap-6">
          <ParameterPanel title="Design B" design={designB} onChange={setDesignB} />
          <section className="panel p-6">
            <h3 className="text-xl font-semibold text-slate-950">Load example into Design B</h3>
            <div className="mt-4 grid gap-3">
              {examples.map((example) => (
                <button
                  key={example.label}
                  type="button"
                  onClick={() => setDesignB(example)}
                  className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-left text-sm text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
                >
                  {example.label}
                </button>
              ))}
            </div>
          </section>
        </div>
      </div>

      {loading ? (
        <section className="panel p-6 text-sm text-slate-600">Loading comparison inputs…</section>
      ) : (
        <ScenarioPicker
          scenarios={scenarios}
          selectedScenario={localScenario}
          onChange={(scenario) => {
            setLocalScenario(scenario);
            setCurrentScenario(scenario);
          }}
        />
      )}

      <section className="panel flex flex-col gap-4 p-6 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h3 className="text-xl font-semibold text-slate-950">Run shared scenario</h3>
          <p className="mt-2 text-sm text-slate-600">Both designs receive the exact same scenario id and parameter payload.</p>
        </div>
        <button type="button" className="action-button" disabled={submitting || !localScenario} onClick={runComparison}>
          {submitting ? "Running comparison…" : "Run comparison"}
        </button>
      </section>

      {error ? <section className="panel border border-rose-200 bg-rose-50 p-6 text-sm text-rose-700">{error}</section> : null}

      {compareResult ? (
        <>
          <CompareTable
            result={compareResult}
            designALabel={designA.label || "Design A"}
            designBLabel={designB.label || "Design B"}
          />
          <section className="grid gap-6 xl:grid-cols-2">
            <PegPriceChart primary={compareResult.design_a_result.timeseries} secondary={compareResult.design_b_result.timeseries} />
            <CollateralRatioChart
              primary={compareResult.design_a_result.timeseries}
              secondary={compareResult.design_b_result.timeseries}
            />
            <ReservesChart primary={compareResult.design_a_result.timeseries} secondary={compareResult.design_b_result.timeseries} />
            <SupplyFlowChart primary={compareResult.design_a_result.timeseries} secondary={compareResult.design_b_result.timeseries} />
          </section>
        </>
      ) : null}
    </div>
  );
}

export default ComparePage;
