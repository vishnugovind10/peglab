import type { Design } from "../types";

const STORAGE_KEY = "peglab.design";

export function saveDesign(design: Design): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(design));
}

export function loadDesign(): Design | null {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw) as Design;
  } catch {
    return null;
  }
}
