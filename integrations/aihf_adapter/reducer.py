from typing import List, Dict, Tuple
from .schema import Signal, Intent
from .config import AGENT_WEIGHTS, MIN_CONFIDENCE, INTENT_TTL_SEC

def _fam(src: str) -> str:
    s = src.lower()
    if "valuation" in s: return "valuation"
    if "macro" in s or "druckenmiller" in s: return "macro"
    if "technical" in s: return "technical"
    if "sentiment" in s: return "sentiment"
    return "valuation"

def reduce_signals(signals: List[Signal]) -> Tuple[Intent, Dict[str,float]]:
    buckets: Dict[str,float] = {k:0.0 for k in ["BUY","SELL","SHORT","COVER","HOLD"]}
    contrib: Dict[str,float] = {}
    for sig in signals:
        w = AGENT_WEIGHTS.get(_fam(sig.source), 0.0)
        sc = sig.confidence * w
        buckets[sig.side] += sc
        contrib[sig.source] = contrib.get(sig.source, 0.0) + sc
    tot = sum(contrib.values()) or 1.0
    for k in list(contrib.keys()): contrib[k] /= tot
    side = max(buckets.items(), key=lambda kv: kv[1])[0]
    denom = sum(buckets.values()) or 1.0
    conf = (buckets[side] / denom) if denom else 0.0
    if conf < MIN_CONFIDENCE: side = "HOLD"
    rats = []
    for src,_ in sorted(contrib.items(), key=lambda kv: kv[1], reverse=True)[:4]:
        r = next((s.rationale for s in signals if s.source==src), "")
        rats.append(f"{src}: {r[:240]}")
    rationale = " | "; rationale = rationale.join(rats) if rats else "no-rationale"
    intent = Intent.new(signals[0].symbol if signals else "UNKNOWN", side, conf,
                        rationale, contrib, INTENT_TTL_SEC, {"buckets": buckets})
    return intent, buckets
