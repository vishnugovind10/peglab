# Adding a Collateral Model

1. Create a new model class in `engine/peglab_engine/models/`.
2. Implement `initial_state()` and `step()`.
3. Register the model in `engine/peglab_engine/models/__init__.py`.
4. Add model assumptions in `engine/peglab_engine/assumptions.py`.
5. Extend backend and frontend enums if the new model is part of the supported UI surface.
