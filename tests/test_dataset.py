import pandas as pd

from eu4m_workshop import (
    PART_NAMES,
    SimulationConfig,
    dataframe_sha256,
    file_sha256,
    load_dataset,
    simulate_dataset,
    to_canonical_csv,
)


def small_dataset() -> pd.DataFrame:
    return simulate_dataset(SimulationConfig(duration_s=1.0, runs_per_scenario=1))


def test_canonical_csv_uses_lf_and_eight_decimals():
    payload = to_canonical_csv(small_dataset())
    assert b"\r" not in payload
    assert payload.splitlines()[1].split(b",")[3] == b"0.00000000"


def test_hash_is_stable_for_equal_frames():
    assert dataframe_sha256(small_dataset()) == dataframe_sha256(small_dataset())


def test_file_hash_ignores_crlf(tmp_path):
    lf = tmp_path / "lf.csv"
    crlf = tmp_path / "crlf.csv"
    lf.write_bytes(to_canonical_csv(small_dataset()))
    crlf.write_bytes(lf.read_bytes().replace(b"\n", b"\r\n"))
    assert file_sha256(lf) == file_sha256(crlf) == dataframe_sha256(small_dataset())


def test_load_dataset_concatenates_parts_in_scenario_order(tmp_path):
    frame = small_dataset()
    for scenario, name in zip(("nominal", "actuator_loss", "sensor_bias"), PART_NAMES):
        (tmp_path / name).write_bytes(to_canonical_csv(frame[frame["scenario"] == scenario]))
    loaded = load_dataset(tmp_path)
    assert loaded["scenario"].drop_duplicates().tolist() == ["nominal", "actuator_loss", "sensor_bias"]
    assert dataframe_sha256(loaded) == dataframe_sha256(frame)
