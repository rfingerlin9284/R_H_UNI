# PR Summary for Test & CI Improvements

This PR includes:

- Added unit tests for `util.retry` and `util.logging`.
- Added test to verify stochastic jitter in `wolf_packs.stochastic_config`.
- Added `tests/conftest.py` to ensure the repository root is on `sys.path` during pytest runs.
- Added `scripts/prepare_training.py` + `docs/TRAINING.md` to prepare GS artifacts for training.
- Updated `.github/workflows/gs-check.yml` to cache pip installs, run the GS battery, and upload artifacts from both `UNIBOT_reports` and `artifacts/`.
- Added a short GS test summary to `README.md`.
- Cleaned up `requirements.txt` duplicate entries.

Why

These changes improve test coverage, make CI more reliable, and add a small training scaffold to convert GS test artifacts into a consumable JSON for downstream analysis.

How to test locally

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest -q
python3 scripts/prepare_training.py --out training_data
```

Notes

- The CI workflow was updated; trigger a build (push branch or run `workflow_dispatch`) to validate the changes in GitHub Actions.
