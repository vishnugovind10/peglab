import { Link } from "react-router-dom";

import AssumptionsBanner from "../components/AssumptionsBanner";
import MetricsCard from "../components/MetricsCard";
import CollateralRatioChart from "../components/charts/CollateralRatioChart";
import PegPriceChart from "../components/charts/PegPriceChart";
import ReservesChart from "../components/charts/ReservesChart";
import SupplyFlowChart from "../components/charts/SupplyFlowChart";
import { useAppContext } from "../context/AppContext";

function ResultsPage() {
  const { currentDesign, lastResult } = useAppContext();

  if (!lastResult) {
    return (
      <section className="panel p-6">
        <h2 className="text-2xl font-semibold text-slate-950">No simulation result yet.</h2>
        <p className="mt-2 text-sm text-slate-600">
          Start from the stress test page to generate a result for {currentDesign.label || currentDesign.collateral_model}.
        </p>
        <Link className="mt-5 inline-flex rounded-full bg-slate-950 px-4 py-2 text-sm font-medium text-white" to="/stress">
          Go to stress test
        </Link>
      </section>
    );
  }

  const failureTone =
    lastResult.failure_probability === "low"
      ? "good"
      : lastResult.failure_probability === "medium"
        ? "warning"
        : "neutral";

  return (
    <div className="grid gap-6">
      <AssumptionsBanner assumptions={lastResult.assumptions} />

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <MetricsCard label="Peg stability" value={`${lastResult.peg_stability_pct}%`} tone="good" />
        <MetricsCard
          label="Recovery time"
          value={lastResult.recovery_time_steps === null ? "No recovery" : `${lastResult.recovery_time_steps} steps`}
        />
        <MetricsCard label="Worst drawdown" value={`${lastResult.worst_drawdown_pct}%`} tone="warning" />
        <MetricsCard label="Collateral ratio" value={lastResult.final_collateral_ratio.toFixed(2)} />
        <MetricsCard label="Failure probability" value={lastResult.failure_probability} tone={failureTone} />
      </section>

      <section className="grid gap-6 xl:grid-cols-2">
        <PegPriceChart primary={lastResult.timeseries} />
        <CollateralRatioChart primary={lastResult.timeseries} />
        <ReservesChart primary={lastResult.timeseries} />
        <SupplyFlowChart primary={lastResult.timeseries} />
      </section>

      <section className="panel p-6">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <p className="eyebrow">Recommendations</p>
            <h2 className="mt-3 text-2xl font-semibold text-slate-950">Rule-based next steps</h2>
          </div>
          <Link className="action-button inline-flex items-center justify-center no-underline" to="/compare">
            Compare against another design
          </Link>
        </div>
        <div className="mt-6 grid gap-3">
          {lastResult.recommendations.map((recommendation) => (
            <div key={recommendation} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm leading-6 text-slate-700">
              {recommendation}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default ResultsPage;
