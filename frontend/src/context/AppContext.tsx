import { createContext, useContext, useState, type PropsWithChildren } from "react";

import { createDefaultDesign, type CompareResponse, type Design, type ScenarioSelection, type SimulationResult } from "../types";
import { loadDesign, saveDesign } from "../lib/storage";

interface AppContextValue {
  currentDesign: Design;
  setCurrentDesign: (design: Design) => void;
  currentScenario: ScenarioSelection | null;
  setCurrentScenario: (scenario: ScenarioSelection | null) => void;
  lastResult: SimulationResult | null;
  setLastResult: (result: SimulationResult | null) => void;
  compareResult: CompareResponse | null;
  setCompareResult: (result: CompareResponse | null) => void;
}

const AppContext = createContext<AppContextValue | null>(null);

export function AppProvider({ children }: PropsWithChildren) {
  const [currentDesign, setCurrentDesignState] = useState<Design>(() => loadDesign() ?? createDefaultDesign());
  const [currentScenario, setCurrentScenario] = useState<ScenarioSelection | null>(null);
  const [lastResult, setLastResult] = useState<SimulationResult | null>(null);
  const [compareResult, setCompareResult] = useState<CompareResponse | null>(null);

  const setCurrentDesign = (design: Design) => {
    saveDesign(design);
    setCurrentDesignState(design);
  };

  return (
    <AppContext.Provider
      value={{
        currentDesign,
        setCurrentDesign,
        currentScenario,
        setCurrentScenario,
        lastResult,
        setLastResult,
        compareResult,
        setCompareResult,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useAppContext must be used within AppProvider");
  }
  return context;
}
