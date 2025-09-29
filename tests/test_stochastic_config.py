import sys
import pathlib
import math

# ensure repo root is on sys.path (conftest.py already does this, but keep local safety)
repo_root = pathlib.Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from wolf_packs.stochastic_config import load_thresholds


def is_numeric(v):
    return isinstance(v, (int, float))


def test_thresholds_jitter_by_default():
    base = load_thresholds()
    second = load_thresholds()

    # if loader returned empty (missing file) skip test
    if not base or not second:
        return

    numeric_keys = [k for k, v in base.items() if is_numeric(v)]
    if not numeric_keys:
        return

    diffs = []
    for k in numeric_keys:
        a = float(base.get(k))
        b = float(second.get(k))
        if math.isclose(a, b, rel_tol=1e-12, abs_tol=0.0):
            continue
        diffs.append(k)

    assert diffs, f"Expected at least one numeric threshold to jitter between loads; none changed. Keys: {numeric_keys}"
