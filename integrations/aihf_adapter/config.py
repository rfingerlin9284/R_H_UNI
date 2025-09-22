#!/usr/bin/env python3
"""Configuration for the AIHF file-queue adapter.

All values may be overridden with environment variables. Defaults are set
to reasonable local paths under the project ROOT.
"""
import json
import os
from typing import Any, Dict


def _j(name: str, default: Dict[str, Any]) -> Dict[str, Any]:
    try:
        return json.loads(os.environ.get(name, "")) if os.environ.get(name) else default
    except Exception:
        return default


ROOT = os.environ.get("RICK_ROOT") or os.getcwd()

AGENT_WEIGHTS = _j("AIHF_AGENT_WEIGHTS", {"valuation": 0.4, "macro": 0.3, "technical": 0.2, "sentiment": 0.1})
MIN_CONFIDENCE = float(os.environ.get("AIHF_MIN_CONFIDENCE", "0.55"))
INTENT_TTL_SEC = int(os.environ.get("AIHF_INTENT_TTL_SEC", "900"))

def _under_root(path: str) -> str:
    """Force any path to live under ROOT; if outside, rebase to ROOT/runtime/"""
    path = os.path.abspath(path)
    root_abs = os.path.abspath(ROOT)
    if not path.startswith(root_abs):
        return os.path.join(root_abs, "runtime", os.path.basename(path))
    return path

INBOX_DIR = _under_root(os.environ.get("AIHF_INBOX_DIR") or os.path.join(ROOT, "runtime", "aihf_inbox"))
# Named consistently for this adapter; consumers should set `AIHF_INTENT_OUTBOX` if they want custom location
INTENT_OUTBOX = _under_root(os.environ.get("AIHF_INTENT_OUTBOX") or os.path.join(ROOT, "runtime", "intent_inbox"))

# Create directories proactively (under project root)
os.makedirs(INBOX_DIR, exist_ok=True)
os.makedirs(INTENT_OUTBOX, exist_ok=True)
