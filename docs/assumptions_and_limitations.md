# Assumptions and Limitations

PegLab v1 is a simplified deterministic stress-testing tool, not a market simulator.

It does not model:

- Live oracle feeds or exchange connectivity
- Real market microstructure or order-book dynamics
- Endogenous trader behavior beyond fixed demand and redemption responses
- Governance processes beyond a simple delayed-response stress case
- Cross-venue arbitrage, funding markets, or legal redemption constraints

It does model:

- Fixed collateral configurations
- Explicit redemption throughput limits
- Deterministic shock timing
- Simplified liquidation effects for crypto-backed systems
- Scenario-specific assumptions that are returned with every simulation result
