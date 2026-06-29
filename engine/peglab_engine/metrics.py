from __future__ import annotations

from peglab_engine.types import SimState, SimulationResult, TimeseriesData


def _round(value: float) -> float:
    return round(value, 2)


def compute_peg_stability_pct(states: list[SimState], tolerance: float = 0.02) -> float:
    stable_steps = sum(1 for state in states if abs(state.peg_price - 1.0) <= tolerance)
    return _round(100 * stable_steps / max(len(states), 1))


def compute_recovery_time_steps(
    states: list[SimState],
    breach_tolerance: float = 0.02,
    recovery_tolerance: float = 0.01,
    recovery_window: int = 5,
) -> int | None:
    breach_index = next(
        (index for index, state in enumerate(states) if abs(state.peg_price - 1.0) > breach_tolerance),
        None,
    )
    if breach_index is None:
        return 0

    for index in range(breach_index + 1, len(states) - recovery_window + 1):
        window = states[index : index + recovery_window]
        if all(abs(state.peg_price - 1.0) <= recovery_tolerance for state in window):
            return index - breach_index
    return None


def compute_worst_drawdown_pct(states: list[SimState]) -> float:
    worst = max((max(0.0, 1.0 - state.peg_price) for state in states), default=0.0)
    return _round(worst * 100)


def build_failure_probability(
    peg_stability_pct: float,
    recovery_time_steps: int | None,
    worst_drawdown_pct: float,
    final_collateral_ratio: float,
) -> str:
    risk_score = 0
    if peg_stability_pct < 85:
        risk_score += 1
    if peg_stability_pct < 65:
        risk_score += 1
    if worst_drawdown_pct > 5:
        risk_score += 1
    if worst_drawdown_pct > 12:
        risk_score += 1
    if recovery_time_steps is None or recovery_time_steps > 25:
        risk_score += 2
    if final_collateral_ratio < 1.0:
        risk_score += 2
    elif final_collateral_ratio < 1.1:
        risk_score += 1

    if risk_score >= 5:
        return "high"
    if risk_score >= 3:
        return "medium"
    return "low"


def build_recommendations(
    peg_stability_pct: float,
    recovery_time_steps: int | None,
    worst_drawdown_pct: float,
    final_collateral_ratio: float,
) -> list[str]:
    recommendations: list[str] = []

    if peg_stability_pct < 85:
        recommendations.append("Increase reserve buffers or tighten mint issuance to improve peg stability.")
    if worst_drawdown_pct > 5:
        recommendations.append("Increase redemption throughput or secondary liquidity support during stress.")
    if recovery_time_steps is None:
        recommendations.append("Raise reserve ratio or liquidation responsiveness; the peg did not recover in the test window.")
    elif recovery_time_steps > 20:
        recommendations.append("Reduce oracle delay or governance response latency to shorten recovery time.")
    if final_collateral_ratio < 1.0:
        recommendations.append("Increase starting collateralization or reduce exposure to inaccessible collateral.")
    elif final_collateral_ratio < 1.1:
        recommendations.append("Add a larger collateral buffer to keep the system above minimum coverage.")

    if not recommendations:
        recommendations.append("Maintain current parameters and monitor stress assumptions against live design changes.")
    return recommendations


def build_simulation_result(states: list[SimState], assumptions: list[str]) -> SimulationResult:
    timeseries = TimeseriesData()
    for state in states:
        timeseries.append(state)

    peg_stability_pct = compute_peg_stability_pct(states)
    recovery_time_steps = compute_recovery_time_steps(states)
    worst_drawdown_pct = compute_worst_drawdown_pct(states)
    final_collateral_ratio = _round(states[-1].collateral_ratio if states else 1.0)
    failure_probability = build_failure_probability(
        peg_stability_pct,
        recovery_time_steps,
        worst_drawdown_pct,
        final_collateral_ratio,
    )
    recommendations = build_recommendations(
        peg_stability_pct,
        recovery_time_steps,
        worst_drawdown_pct,
        final_collateral_ratio,
    )

    return SimulationResult(
        peg_stability_pct=peg_stability_pct,
        recovery_time_steps=recovery_time_steps,
        worst_drawdown_pct=worst_drawdown_pct,
        final_collateral_ratio=final_collateral_ratio,
        failure_probability=failure_probability,
        recommendations=recommendations,
        timeseries=timeseries,
        assumptions=assumptions,
    )
