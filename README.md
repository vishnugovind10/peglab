# peglab

> **Stable-Asset Stress-Testing Lab**: Design a stablecoin's collateral mechanism, run it against ten fixed adverse scenarios, and get back the same deterministic risk metrics every time — before a single line of production code exists.

## The Thesis: Design Choices Nobody Pressure-Tests

Stablecoin teams pick a collateral model — fiat-backed, crypto-backed, overcollateralized — largely on precedent: "USDC does it this way," "MakerDAO does it that way." The actual behavior of that choice under a bank run, an oracle outage, or a collateral crash is rarely quantified before deployment, because building a real simulation harness is its own project and nobody wants to build one just to validate a parameter sheet.

`peglab` exists to make that pressure-test cheap and repeatable. It takes a design (collateral model plus its parameters), runs it through a pure-Python simulation engine against fixed, explicit stress scenarios — bank runs, whale redemptions, oracle failure, collateral crashes, bridge failure, governance failure, black swans, and more — and reports the same four risk metrics every time, regardless of which model or scenario was chosen. The result is not a market forecast and not a claim about how the real asset will behave under real market conditions. It is a bounded, deterministic instrument for comparing design decisions against each other before they're load-bearing.

## Core Metrics Defined

Every simulation run reduces to four numbers, computed identically across all collateral models and scenarios:

- **Peg Stability (%)**: The percentage of simulated steps where `|peg_price - 1.0| <= 0.02`. A design that spends most of the run within 2% of peg scores high; one that drifts scores low.
- **Recovery Time (steps)**: The number of steps between the first peg breach (`|peg_price - 1.0| > 0.02`) and the first sustained window of 5 consecutive steps within 1% of peg. `0` means the peg never broke; `null` means it never recovered within the simulation window.
- **Worst Drawdown (%)**: `max(0, 1 - peg_price) * 100` across the entire run — the deepest single-step deviation below peg.
- **Final Collateral Ratio**: The collateral ratio at the last simulated step, i.e. what's left standing after the scenario plays out.

These four feed a rule-based **Failure Probability** (`low` / `medium` / `high`), scored from fixed thresholds on stability, drawdown, recovery time, and final collateralization — deliberately simple and auditable rather than a black-box model.

## Quickstart

Run a simulation without the web stack:

```bash
python -m pip install -e engine[dev]
cd examples
python run_example.py --config usdc_style_config.json --scenario bank_run
python run_example.py --config makerdao_style_config.json --scenario collateral_crash
```

This prints the four core metrics, the failure probability, and scenario-specific recommendations as JSON.

Run the full stack (design UI, compare view, charts):

```bash
python -m pip install -e engine[dev]
python -m pip install -e backend[dev]
cd frontend && npm install

cd engine && pytest -q
cd ../backend && uvicorn app.main:app --reload
cd ../frontend && npm run dev
```

## Architecture

```text
Frontend (React + TypeScript + Recharts)
  - Design configurator
  - Stress test runner
  - Results dashboard
  - Compare view
            |
            | JSON over HTTP
            v
Backend (FastAPI)
  - GET  /scenarios
  - GET  /designs/examples
  - POST /simulate
  - POST /compare
            |
            v
Simulation Engine (pure Python, no FastAPI/frontend dependency)
  - collateral models: fiat-backed, crypto-backed, overcollateralized
  - 10 fixed stress scenarios
  - deterministic step loop
  - rule-based metrics
```

The engine is stateless and framework-free by design — `engine/peglab_engine/engine.py`'s `SimulationEngine.run()` takes a design and a scenario id, steps a `CollateralModel` forward through fixed per-step shocks from a `Scenario`, and reduces the resulting state trajectory to the four core metrics plus assumptions. The backend is a thin, stateless FastAPI wrapper around that engine. The frontend persists saved designs in browser `localStorage` — there is no server-side project store.

## Scope / What This Is Not

`peglab` is a simplified, deterministic stress-testing tool, not a market simulator. It does not model:

- Live oracle feeds or exchange connectivity
- Real market microstructure or order-book dynamics
- Endogenous trader behavior beyond fixed demand and redemption responses
- Governance processes beyond a simple delayed-response stress case
- Cross-venue arbitrage, funding markets, or legal redemption constraints

It does model fixed collateral configurations, explicit redemption throughput limits, deterministic shock timing, simplified liquidation effects for crypto-backed systems, and scenario-specific assumptions returned alongside every result. See [docs/assumptions_and_limitations.md](docs/assumptions_and_limitations.md) for the full boundary list.

## Development

```bash
python -m pip install -e engine[dev]
python -m pip install -e backend[dev]
cd frontend && npm install

cd engine && pytest -q
cd ../backend && pytest -q
```

Keep changes scoped to the active v1 roadmap and preserve the separation between the pure engine, the API wrapper, and the frontend. See [CONTRIBUTING.md](CONTRIBUTING.md) and [ARCHITECTURE.md](ARCHITECTURE.md).
