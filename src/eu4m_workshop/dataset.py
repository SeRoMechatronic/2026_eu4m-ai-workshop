"""Canonical CSV serialization and integrity hashes for the workshop dataset.

Every hash recorded in ``data/metadata.json`` is computed over bytes written with
LF line endings and eight decimals. Fixing both here keeps the values identical on
Linux, macOS, Windows and Colab.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

from .simulation import SCENARIOS


CSV_OPTIONS = {"index": False, "float_format": "%.8f", "lineterminator": "\n"}
PART_NAMES = tuple(f"actuator_signals_{scenario}.csv" for scenario in SCENARIOS)


def to_canonical_csv(df: pd.DataFrame) -> bytes:
    """Serialize a frame with LF endings and eight decimals on every platform."""
    return df.to_csv(**CSV_OPTIONS).encode("utf-8")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def dataframe_sha256(df: pd.DataFrame) -> str:
    """Hash of the canonical CSV form of ``df``."""
    return sha256_bytes(to_canonical_csv(df))


def file_sha256(path: str | Path) -> str:
    """Hash a text file ignoring CRLF, so a Windows checkout matches the record."""
    return sha256_bytes(Path(path).read_bytes().replace(b"\r\n", b"\n"))


def load_dataset(data_dir: str | Path) -> pd.DataFrame:
    """Rebuild the combined dataset from the three per-scenario CSV files."""
    folder = Path(data_dir)
    return pd.concat(
        [pd.read_csv(folder / name) for name in PART_NAMES], ignore_index=True
    )
