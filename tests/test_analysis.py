import numpy as np
import pandas as pd
import pytest

from eu4m_workshop import build_run_features, build_scenario_summary, simulate_dataset


@pytest.fixture(scope="module")
def features():
    return build_run_features(simulate_dataset())


def test_feature_shape(features):
    assert features.shape == (24, 8)
    assert not features.isna().any().any()


def test_sensor_bias_is_visible_in_validation_residual(features):
    medians = build_scenario_summary(features).set_index("scenario")
    assert medians.loc["sensor_bias", "mean_sensor_residual_m"] > 0.10
    assert abs(medians.loc["nominal", "mean_sensor_residual_m"]) < 0.01


def test_actuator_loss_increases_true_tracking_error(features):
    medians = build_scenario_summary(features).set_index("scenario")
    assert (
        medians.loc["actuator_loss", "tracking_rmse_true_m"]
        > medians.loc["nominal", "tracking_rmse_true_m"]
    )


def test_sensor_bias_hides_true_error_from_measured_error(features):
    row = build_scenario_summary(features).set_index("scenario").loc["sensor_bias"]
    assert row["tracking_rmse_true_m"] > row["tracking_rmse_measured_m"]


def test_missing_column_rejected():
    with pytest.raises(ValueError, match="Missing columns"):
        build_run_features(pd.DataFrame({"run_id": ["x"]}))


def test_empty_dataset_rejected():
    df = simulate_dataset().iloc[0:0]
    with pytest.raises(ValueError, match="empty"):
        build_run_features(df)


def test_outputs_are_finite(features):
    numeric = features.select_dtypes(include=[np.number])
    assert np.isfinite(numeric.to_numpy()).all()


def test_saturation_threshold_follows_the_force_limit():
    dataset = simulate_dataset()
    default = build_run_features(dataset)
    higher_limit = build_run_features(dataset, force_limit_n=1000.0)
    assert default["force_saturation_fraction"].max() > 0
    assert (higher_limit["force_saturation_fraction"] == 0).all()

