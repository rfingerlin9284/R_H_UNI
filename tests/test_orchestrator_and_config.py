import sys
import pathlib

# ensure repo root on sys.path
repo_root = pathlib.Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from wolf_packs import orchestrator
import json


def test_detect_regime_callable():
    assert hasattr(orchestrator, 'detect_regime')
    assert callable(orchestrator.detect_regime)


def test_wolfpack_config_valid_json():
    p = pathlib.Path(__file__).resolve().parents[1] / 'configs' / 'wolfpack_config.json'
    assert p.exists(), f"Expected config at {p}"
    data = json.loads(p.read_text(encoding='utf-8'))
    assert 'enabled' in data
