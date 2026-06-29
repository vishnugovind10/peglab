import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import ScenarioPicker from "../components/ScenarioPicker";
import { useAppContext } from "../context/AppContext";
import { fetchScenarios, simulateDesign } from "../lib/api";
import type { ScenarioMetadata, ScenarioSelection } from "../types";

function StressTestPage() {
  const navigate = useNavigate();
  const { currentDesign, currentScenario, setCurrentScenario, setLastResult, setCompareResult } = useAppContext();
  const [scenarios, setScenarios] = useState<ScenarioMetadata[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    fetchScenarios()
      .then((payload) => {
        if (!active) {
          return;
        }
        setScenarios(payload);
        if (!currentScenario && payload[0]) {
          setCurrentScenario({ id: payload[0].id, params: { ...payload[0].defaults } });
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
  }, [currentScenario, setCurrentScenario]);

  const handleScenarioChange = (scenario: ScenarioSelection) => {
    setCurrentScenario(scenario);
  };

  const runSimulation = async () => {
    if (!currentScenario) {
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      const result = await simulateDesign(currentDesign, currentScenario);
      setLastResult(result);
      setCompareResult(null);
      navigate("/results");
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Simulation failed.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="grid gap-6">
      <section className="panel p-6">
        <p className="eyebrow">2. Stress Test</p>
        <h2 className="mt-3 text-3xl font-semibold text-slate-950">Run a fixed adverse scenario.</h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600">
          Scenario timing is deterministic by design. The exposed sliders and inputs are the only parameters applied.
        </p>
      </section>

      {loading ? (
        <section className="panel p-6 text-sm text-slate-600">Loading scenario library…</section>
      ) : (
        <ScenarioPicker scenarios={scenarios} selectedScenario={currentScenario} onChange={handleScenarioChange} />
      )}

      <section className="panel flex flex-col gap-4 p-6 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h3 className="text-xl font-semibold text-slate-950">Ready to simulate</h3>
          <p className="mt-2 text-sm text-slate-600">The backend is stateless; the full design and scenario are sent on each run.</p>
        </div>
        <button type="button" className="action-button" disabled={submitting || !currentScenario} onClick={runSimulation}>
          {submitting ? "Running simulation…" : "Run stress test"}
        </button>
      </section>

      {error ? <section className="panel border border-rose-200 bg-rose-50 p-6 text-sm text-rose-700">{error}</section> : null}
    </div>
  );
}

export default StressTestPage;
