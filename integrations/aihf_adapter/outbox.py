import time, pathlib, json
from .schema import Intent
from .config import INTENT_OUTBOX


def publish_intent(intent: Intent) -> bool:
    """Write the intent JSON into the configured outbox directory."""
    outdir = pathlib.Path(INTENT_OUTBOX)
    outdir.mkdir(parents=True, exist_ok=True)
    path = outdir / f"{int(time.time())}-{intent.id}.json"
    try:
        with open(path, "w") as f:
            json.dump(intent.__dict__, f, ensure_ascii=False)
        print(f"[aihf_adapter] wrote intent to {path}", flush=True)
        return True
    except Exception as e:
        print(f"[aihf_adapter] failed to write intent: {e}", flush=True)
        return False
