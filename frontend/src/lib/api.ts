import type { CompareResponse, Design, ScenarioMetadata, ScenarioSelection, SimulationResult } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

async function readJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function fetchScenarios(): Promise<ScenarioMetadata[]> {
  const response = await fetch(`${API_BASE_URL}/scenarios`);
  return readJson<ScenarioMetadata[]>(response);
}

export async function fetchExampleDesigns(): Promise<Design[]> {
  const response = await fetch(`${API_BASE_URL}/designs/examples`);
  return readJson<Design[]>(response);
}

export async function simulateDesign(
  design: Design,
  scenario: ScenarioSelection,
  numSteps = 100,
): Promise<SimulationResult> {
  const response = await fetch(`${API_BASE_URL}/simulate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ design, scenario, num_steps: numSteps }),
  });
  return readJson<SimulationResult>(response);
}

export async function compareDesigns(
  designA: Design,
  designB: Design,
  scenario: ScenarioSelection,
  numSteps = 100,
): Promise<CompareResponse> {
  const response = await fetch(`${API_BASE_URL}/compare`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      design_a: designA,
      design_b: designB,
      scenario,
      num_steps: numSteps,
    }),
  });
  return readJson<CompareResponse>(response);
}
