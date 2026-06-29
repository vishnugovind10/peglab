import { NavLink, Route, Routes } from "react-router-dom";

import { useAppContext } from "./context/AppContext";
import { modelLabels } from "./types";
import ComparePage from "./pages/ComparePage";
import DesignPage from "./pages/DesignPage";
import ResultsPage from "./pages/ResultsPage";
import StressTestPage from "./pages/StressTestPage";

function App() {
  const { currentDesign, currentScenario } = useAppContext();

  return (
    <div className="min-h-screen px-4 py-6 text-slate-950 sm:px-6 lg:px-10">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 grid gap-6 rounded-[2rem] border border-white/60 bg-white/80 p-6 shadow-[0_20px_80px_rgba(15,23,42,0.08)] backdrop-blur">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl">
              <p className="eyebrow">PegLab</p>
              <h1 className="mt-3 text-4xl font-semibold tracking-tight text-slate-950 sm:text-5xl">
                Stable asset design under stress.
              </h1>
              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-700 sm:text-lg">
                Configure a mechanism, run it through fixed adverse scenarios, and compare resilience with visible
                assumptions on every result.
              </p>
            </div>
            <div className="grid gap-2 rounded-3xl border border-slate-200 bg-slate-950 px-5 py-4 text-sm text-slate-100">
              <span className="text-slate-400">Active design</span>
              <strong className="text-lg text-white">{currentDesign.label || modelLabels[currentDesign.collateral_model]}</strong>
              <span>{modelLabels[currentDesign.collateral_model]}</span>
              {currentScenario ? <span>Scenario: {currentScenario.id.replaceAll("_", " ")}</span> : null}
            </div>
          </div>
          <nav className="flex flex-wrap gap-3">
            {[
              ["/", "Design"],
              ["/stress", "Stress Test"],
              ["/results", "Results"],
              ["/compare", "Compare"],
            ].map(([to, label]) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `rounded-full px-4 py-2 text-sm font-medium transition ${
                    isActive
                      ? "bg-amber-300 text-slate-950 shadow-[0_10px_25px_rgba(245,158,11,0.35)]"
                      : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                  }`
                }
              >
                {label}
              </NavLink>
            ))}
          </nav>
        </header>

        <Routes>
          <Route path="/" element={<DesignPage />} />
          <Route path="/stress" element={<StressTestPage />} />
          <Route path="/results" element={<ResultsPage />} />
          <Route path="/compare" element={<ComparePage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
