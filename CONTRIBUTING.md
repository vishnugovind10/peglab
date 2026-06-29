# Contributing

1. Install the engine in editable mode with `pip install -e engine[dev]`.
2. Install backend dependencies with `pip install -e backend[dev]`.
3. Install frontend dependencies with `npm install` in `frontend/`.
4. Run `pytest` in `engine/` and `backend/` before opening a pull request.

Keep changes scoped to the active v1 roadmap and preserve the separation between the pure engine, the API wrapper, and the frontend.
