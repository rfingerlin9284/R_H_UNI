# AIHF Adapter

Minimal adapter to ingest decision JSON files from a filesystem inbox and publish normalized intents to an outbox.

Environment variables (defaults shown):

- `AIHF_INBOX_DIR` — path to inbox directory (default: `runtime/aihf_inbox` under project root)
- `AIHF_INTENT_OUTBOX` — path to intent outbox directory (default: `runtime/intent_inbox` under project root)
- `AIHF_MIN_CONFIDENCE` — minimum confidence threshold (default: `0.55`)

Running locally (development):

```bash
export AIHF_INBOX_DIR=/tmp/aihf_inbox
export AIHF_INTENT_OUTBOX=/tmp/aihf_outbox
PYTHONPATH=. python3 -m integrations.aihf_adapter.aihf_adapter
```

Files:
- `aihf_adapter.py` — main runner
- `ingest.py` — filesystem ingest helpers
- `reducer.py` — signal reduction into an intent
- `outbox.py` — publish intent to outbox

For development, see `requirements.txt` in this directory for optional runtime dependencies.
# AIHF Adapter (file-queue only)

This adapter ingests PoC-style decision JSON files from `~/.aihf/inbox/`,
reduces per-agent signals via weighted vote, and writes normalized intents to
`/home/ing/RICK/R_U_UNI/runtime/intent_inbox/`.

- No HTTP bridge. Fully local, offline-capable.
- TTL, contributors, and rationale recorded in each intent.

Quick start (dev):

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install watchdog
python -m integrations.aihf_adapter.aihf_adapter
```

Smoke feed:

```bash
mkdir -p ~/.aihf/inbox
cat > ~/.aihf/inbox/decision-sample.json <<EOF
{"symbol":"AAPL","action":"BUY","confidence":0.78,"rationale":"demo",
 "agents":[{"name":"valuation","confidence":0.85},{"name":"technical","confidence":0.62}]}
EOF
```

Check intents at `runtime/intent_inbox/`.

Headless install (user services):

```bash
chmod +x tools/headless_setup.sh
./tools/headless_setup.sh
```

This creates a venv, installs deps, registers and starts:
- `rick-aihf-adapter.service` (ingests `~/.aihf/inbox`, writes intents to `runtime/intent_inbox`)
- `rick-intent-reader.service` (prints and archives intents; replace with commander consumer)

Service management:

```bash
systemctl --user status rick-aihf-adapter.service
systemctl --user status rick-intent-reader.service
systemctl --user restart rick-aihf-adapter.service
systemctl --user restart rick-intent-reader.service
```
