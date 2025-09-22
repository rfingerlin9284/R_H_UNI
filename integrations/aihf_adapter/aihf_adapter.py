#!/usr/bin/env python3
"""AIHF adapter runner (robust imports, non-blocking exchange recorder).

Usage: run as package or script. Publishes normalized intents to runtime outbox.
"""
from __future__ import annotations

import json
import queue
import time
import subprocess
import os
import sys
import importlib.util


def _ensure_modules():
    """Attempt imports in package, script, and file modes; return the symbols needed."""
    # Determine project paths
    this_dir = os.path.dirname(os.path.abspath(__file__))
    integrations_dir = os.path.dirname(this_dir)
    project_root = os.path.dirname(integrations_dir)

    # First try package relative imports
    try:
        from .ingest import start_ingest_thread, _signals_from_decision
        from .reducer import reduce_signals
        from .outbox import publish_intent
        return start_ingest_thread, _signals_from_decision, reduce_signals, publish_intent
    except Exception:
        pass

    # Next try absolute imports by ensuring project root is on sys.path
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    try:
        from integrations.aihf_adapter.ingest import start_ingest_thread, _signals_from_decision
        from integrations.aihf_adapter.reducer import reduce_signals
        from integrations.aihf_adapter.outbox import publish_intent
        return start_ingest_thread, _signals_from_decision, reduce_signals, publish_intent
    except Exception:
        pass

    # Final fallback: load modules from files and set package context for relative imports
    def _load_pkg_mod(name: str, filename: str):
        full_name = f"integrations.aihf_adapter.{name}"
        path = os.path.join(this_dir, filename)
        spec = importlib.util.spec_from_file_location(full_name, path)
        mod = importlib.util.module_from_spec(spec)
        # so relative imports inside the module work
        mod.__package__ = "integrations.aihf_adapter"
        sys.modules[full_name] = mod
        spec.loader.exec_module(mod)
        return mod

    ingest_mod = _load_pkg_mod("ingest", "ingest.py")
    reducer_mod = _load_pkg_mod("reducer", "reducer.py")
    outbox_mod = _load_pkg_mod("outbox", "outbox.py")

    return (
        getattr(ingest_mod, "start_ingest_thread"),
        getattr(ingest_mod, "_signals_from_decision"),
        getattr(reducer_mod, "reduce_signals"),
        getattr(outbox_mod, "publish_intent"),
    )


def trigger_exchange_recorder(root: str, threshold: int = 5) -> None:
    """Invoke the exchange recorder script in background (non-blocking)."""
    try:
        recorder = os.path.join(root, "tools", "record_exchange.sh")
        if os.path.exists(recorder):
            print(f"[aihf_adapter] recorder path exists: {recorder}", flush=True)
            subprocess.Popen([recorder, str(threshold)], cwd=root)
        else:
            print(f"[aihf_adapter] recorder path NOT found at {recorder}, falling back to relative invocation", flush=True)
            # best-effort: try to run relative path (for legacy setups)
            subprocess.Popen(["/bin/bash", "-lc", f"./tools/record_exchange.sh {threshold}"], cwd=root)
    except Exception:
        # Do not propagate recorder failures
        return


def main() -> None:
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    start_ingest_thread, _signals_from_decision, reduce_signals, publish_intent = _ensure_modules()

    q: queue.Queue = queue.Queue(maxsize=1024)
    start_ingest_thread(q)
    print("[aihf_adapter] started", flush=True)

    while True:
        try:
            dec = q.get(timeout=1.0)
        except queue.Empty:
            continue

        try:
            signals = _signals_from_decision(dec)
            if not signals:
                continue
            intent, buckets = reduce_signals(signals)
            published = publish_intent(intent)

            out = {
                "event": "aihf_intent",
                "intent_id": getattr(intent, "id", None),
                "symbol": getattr(intent, "symbol", None),
                "side": getattr(intent, "side", None),
                "confidence": round(getattr(intent, "confidence", 0.0), 4),
                "expires_at": int(getattr(intent, "expires_at", time.time() + 60)),
                "contributors": getattr(intent, "contributors", {}),
                "buckets": buckets,
                "published": bool(published),
            }
            print(json.dumps(out), flush=True)

            # Non-blocking: record an exchange when we successfully publish
            if published:
                trigger_exchange_recorder(ROOT, threshold=5)

        except Exception as exc:  # pragma: no cover - safety net
            print(f"[aihf_adapter] error: {exc}", flush=True)


if __name__ == "__main__":
    main()

