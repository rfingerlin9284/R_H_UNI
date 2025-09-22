from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Dict, Any
import time, uuid


Side = Literal["BUY", "SELL", "SHORT", "COVER", "HOLD"]


@dataclass
class Signal:
    symbol: str
    side: Side
    confidence: float
    weight: float
    rationale: str
    source: str
    ts: float = field(default_factory=lambda: time.time())


@dataclass
class Intent:
    id: str
    symbol: str
    side: Side
    confidence: float
    rationale: str
    contributors: Dict[str, float]
    ttl_sec: int
    expires_at: float
    source: str = "aihf_adapter"
    meta: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def new(symbol, side, confidence, rationale, contributors, ttl_sec, meta=None) -> "Intent":
        now = time.time()
        return Intent(
            str(uuid.uuid4()),
            symbol,
            side,
            confidence,
            rationale,
            contributors,
            ttl_sec,
            now + ttl_sec,
            "aihf_adapter",
            meta or {},
        )
