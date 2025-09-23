Live Rebuild - README

This branch contains template artifacts for a RICK-compliant live trading rebuild.

PIN gating
-----------
- This branch is gated by PIN `841921`. DO NOT run or promote any files in `live/` to production without human approval.

Quick local test steps
---------------------
```bash
cd ~/R_U_UNI
python3 -m venv .venv_live
source .venv_live/bin/activate
pip install -r requirements-dev.txt
# Run deterministic scan (dry-run)
python tools/purge_deterministic.py --root . --out .state/deterministic_findings.json
# Run tests
pytest tests/wolf_packs -q
```

Notes
-----
- The `live/` files are templates and placeholders. Extract exact logic from proven sources before promoting to production.
- This README should appear in the PR for reviewers.
