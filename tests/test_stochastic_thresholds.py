import os
from wolf_packs.stochastic_config import load_thresholds


def test_thresholds_jitter_by_default():
    # The loader should apply jitter on successive calls
    base = load_thresholds()
    # load again -- should typically differ due to jitter
    second = load_thresholds()
    # If the loader returned empty (missing file) just skip assert
    if not base or not second:
        return
    # at least one numeric entry should differ
    diffs = [k for k in base if base.get(k) != second.get(k)]
    assert diffs, f"Expected jitter between successive loads, none found: {base}"

