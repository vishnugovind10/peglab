from peglab_engine.metrics import build_recommendations


def test_recommendations_trigger_for_threshold_breaches():
    recommendations = build_recommendations(
        peg_stability_pct=60.0,
        recovery_time_steps=None,
        worst_drawdown_pct=14.0,
        final_collateral_ratio=0.92,
    )

    assert any("reserve" in recommendation.lower() for recommendation in recommendations)
    assert any("redemption" in recommendation.lower() for recommendation in recommendations)
