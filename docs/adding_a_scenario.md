# Adding a Scenario

1. Create a scenario class in `engine/peglab_engine/scenarios/`.
2. Define `parameter_schema` with bounded defaults.
3. Implement `shock_for_step()`.
4. Register the scenario in `engine/peglab_engine/scenarios/__init__.py`.
5. Add scenario assumptions in `engine/peglab_engine/assumptions.py`.
