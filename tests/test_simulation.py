import pandas as pd
import pytest

from eu4m_workshop import SimulationConfig, simulate_dataset, simulate_run


def test_unknown_scenario_rejected():
    with pytest.raises(ValueError, match="Unknown scenario"):
        simulate_run("unknown", 0)


def test_negative_run_rejected():
    with pytest.raises(ValueError, match="non-negative"):
        simulate_run("nominal", -1)


def test_run_shape_and_columns():
    df = simulate_run("nominal", 0)
    assert len(df) == 400
    assert df["run_id"].nunique() == 1
    assert not df.isna().any().any()
    assert {"reference_m", "position_measured_m", "position_true_m"}.issubset(df.columns)


def test_run_is_deterministic():
    pd.testing.assert_frame_equal(simulate_run("sensor_bias", 3), simulate_run("sensor_bias", 3))


def test_dataset_is_balanced():
    df = simulate_dataset()
    assert len(df) == 9600
    assert df.groupby("scenario")["run_id"].nunique().to_dict() == {
        "actuator_loss": 8,
        "nominal": 8,
        "sensor_bias": 8,
    }


def test_config_changes_number_of_samples():
    cfg = SimulationConfig(duration_s=2.0, dt_s=0.05, runs_per_scenario=1)
    df = simulate_dataset(cfg)
    assert len(df) == 3 * 40

