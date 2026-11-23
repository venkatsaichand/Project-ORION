import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from orion_pipeline import wilson_interval


def test_wilson_interval_is_ordered_and_bounded():
    low, high = wilson_interval(10, 100)
    assert 0 <= low < 0.10 < high <= 1


def test_wilson_interval_empty_denominator():
    low, high = wilson_interval(0, 0)
    assert low != low  # NaN
    assert high != high
