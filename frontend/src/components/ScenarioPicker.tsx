import type { ScenarioMetadata, ScenarioSelection } from "../types";

interface ScenarioPickerProps {
  scenarios: ScenarioMetadata[];
  selectedScenario: ScenarioSelection | null;
  onChange: (scenario: ScenarioSelection) => void;
}

function ScenarioPicker({ scenarios, selectedScenario, onChange }: ScenarioPickerProps) {
  const selectedMetadata = scenarios.find((scenario) => scenario.id === selectedScenario?.id) ?? scenarios[0];

  return (
    <section className="panel p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-slate-950">Stress Scenario</h2>
        <p className="mt-2 text-sm leading-6 text-slate-600">
          Scenarios are fixed in v1. You can tune only the bounded parameters exposed on each card.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {scenarios.map((scenario) => {
          const active = scenario.id === selectedMetadata?.id;
          return (
            <button
              key={scenario.id}
              type="button"
              onClick={() => onChange({ id: scenario.id, params: { ...scenario.defaults } })}
              className={`rounded-[1.5rem] border p-5 text-left transition ${
                active ? "border-teal-300 bg-teal-50" : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50"
              }`}
            >
              <p className="font-semibold text-slate-950">{scenario.name}</p>
              <p className="mt-3 text-sm leading-6 text-slate-600">{scenario.description}</p>
            </button>
          );
        })}
      </div>

      {selectedMetadata ? (
        <div className="mt-6 grid gap-5 md:grid-cols-2 xl:grid-cols-3">
          {selectedMetadata.parameters.map((parameter) => (
            <label key={parameter.id}>
              <span className="field-label">{parameter.label}</span>
              <input
                className="field-input mt-2"
                type="number"
                min={parameter.min}
                max={parameter.max}
                step={parameter.step}
                value={selectedScenario?.params[parameter.id] ?? parameter.default}
                onChange={(event) =>
                  onChange({
                    id: selectedMetadata.id,
                    params: {
                      ...(selectedScenario?.params ?? selectedMetadata.defaults),
                      [parameter.id]:
                        parameter.type === "int" ? Math.round(Number(event.target.value)) : Number(event.target.value),
                    },
                  })
                }
              />
              <span className="field-help">
                Range {parameter.min} to {parameter.max}
              </span>
            </label>
          ))}
        </div>
      ) : null}
    </section>
  );
}

export default ScenarioPicker;
