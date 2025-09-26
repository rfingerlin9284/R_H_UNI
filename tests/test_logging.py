import sys
import pathlib
import json

# Ensure repo root is on sys.path so local packages import during pytest
repo_root = pathlib.Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from util.logging import get_logger


def test_logger_writes_file(tmp_path):
    run_id = "testrun123"
    out_dir = tmp_path / "artifacts"
    logger = get_logger(run_id=run_id, out_dir=str(out_dir), module="test_mod")
    logger.info("hello", {"a": 1})

    f = out_dir / run_id / "logs.jsonl"
    assert f.exists(), f"Expected log file at {f}"
    lines = f.read_text(encoding="utf-8").splitlines()
    assert lines, "Expected at least one log line"
    obj = json.loads(lines[-1])
    assert obj.get("run_id") == run_id
    assert obj.get("module") == "test_mod"
    assert obj.get("msg") == "hello"


def test_logger_no_runid_does_not_create_file(tmp_path):
    out_dir = tmp_path / "out"
    logger = get_logger(run_id=None, out_dir=str(out_dir), module="m")
    logger.info("x")
    # When run_id is None the logger should not create per-run files
    assert not out_dir.exists(), "Out dir should not be created when run_id is None"
