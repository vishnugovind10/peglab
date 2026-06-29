from __future__ import annotations

from abc import ABC, abstractmethod

from peglab_engine.types import ScenarioParameterDefinition, ScenarioShock


class Scenario(ABC):
    id: str
    name: str
    description: str
    parameter_schema: list[ScenarioParameterDefinition]

    def __init__(self, params: dict[str, float | int] | None = None):
        defaults = {parameter.id: parameter.default for parameter in self.parameter_schema}
        self.params = {**defaults, **(params or {})}

    @abstractmethod
    def shock_for_step(self, step: int, num_steps: int) -> ScenarioShock:
        """Return the active shock for a simulation step."""

    def assumptions(self) -> list[str]:
        return [self.description]

    def metadata(self) -> dict[str, object]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "parameters": [parameter.to_dict() for parameter in self.parameter_schema],
            "defaults": self.params,
        }


def within_window(step: int, start: int, duration: int) -> bool:
    return start <= step < start + duration
