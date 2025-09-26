# CI Audit Notes

This document lists suggestions and checks to ensure the GitHub Actions `gs-check.yml` workflow mirrors local runs:

1. Ensure Python version matches local (3.12 used in `setup-python`).
2. Cache pip to speed up runs (implemented).
3. Install dependencies with `python -m pip install -r requirements.txt`.
4. Ensure the GS battery writes artifacts to a predictable location; the workflow copies `$HOME/UNIBOT_reports` into the workspace for upload.
5. Validate artifact upload paths in a test run (use `act` locally or push a branch to trigger CI).
6. Confirm that any environment variable reliance is documented; the project avoids deterministic env vars by design.

Run locally with `act` (optional):

```bash
# install act and run the workflow event 'workflow_dispatch'
act -j gs
```

Note: `act` requires additional setup and may need larger runner images for Python 3.12.
