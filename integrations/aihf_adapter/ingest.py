#!/usr/bin/env python3
from __future__ import annotations
import json, os, time, threading, queue
from typing import Dict, Any, List
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    _HAS_WATCHDOG = True
except Exception:
    Observer = None
    FileSystemEventHandler = object
    _HAS_WATCHDOG = False
from .schema import Signal
from .config import INBOX_DIR

def _map_action_to_side(action: str) -> str:
    a = (action or "").upper()
    if a in {"BUY","SELL","SHORT","COVER","HOLD"}:
        return a
    return "HOLD"

def _signals_from_decision(dec: Dict[str, Any]) -> List[Signal]:
    sym = dec.get("symbol", "UNKNOWN")
    side = _map_action_to_side(dec.get("action", "HOLD"))
    agents = dec.get("agents") or []
    if not agents:
        return [Signal(symbol=sym, side=side, confidence=float(dec.get("confidence", 0.5)),
                       weight=1.0, rationale=dec.get("rationale", ""), source="aihf:unknown")]
    out: List[Signal] = []
    for a in agents:
        name = str(a.get("name", "unknown"))
        conf = float(a.get("confidence", 0.5))
        rat = a.get("rationale", "")
        out.append(Signal(symbol=sym, side=side, confidence=conf, weight=1.0,
                          rationale=rat, source=f"aihf:{name}"))
    return out

if _HAS_WATCHDOG:
    class _Handler(FileSystemEventHandler):
        def __init__(self, q: queue.Queue):
            self.q = q
        def on_created(self, event):
            if event.is_directory:
                return
            if event.src_path.endswith(".json"):
                try:
                    with open(event.src_path, "r") as f:
                        self.q.put(json.load(f))
                except Exception:
                    pass
else:
    # Simple polling fallback when watchdog is unavailable
    class _Handler:
        def __init__(self, q: queue.Queue):
            self.q = q
        def poll_inbox(self, inbox_dir: str):
            # yield all json decisions currently in the inbox
            for fname in sorted([f for f in os.listdir(inbox_dir) if f.endswith(".json")]):
                p = os.path.join(inbox_dir, fname)
                try:
                    with open(p, "r") as f:
                        self.q.put(json.load(f))
                except Exception:
                    pass

def feed_from_inbox(q: queue.Queue) -> None:
    os.makedirs(INBOX_DIR, exist_ok=True)
    # seed existing files
    for fname in sorted([f for f in os.listdir(INBOX_DIR) if f.endswith(".json")]):
        p = os.path.join(INBOX_DIR, fname)
        try:
            with open(p, "r") as f:
                q.put(json.load(f))
        except Exception:
            pass

    if _HAS_WATCHDOG:
        obs = Observer()
        h = _Handler(q)
        obs.schedule(h, INBOX_DIR, recursive=False)
        obs.start()
        try:
            while True:
                time.sleep(1)
        finally:
            obs.stop()
            obs.join()
    else:
        # polling loop
        h = _Handler(q)
        try:
            while True:
                h.poll_inbox(INBOX_DIR)
                time.sleep(1)
        except KeyboardInterrupt:
            return

def start_ingest_thread(q: queue.Queue) -> threading.Thread:
    t = threading.Thread(target=feed_from_inbox, args=(q,), daemon=True)
    t.start(); return t

__all__ = ["start_ingest_thread", "_signals_from_decision"]
