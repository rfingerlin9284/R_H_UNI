# Preparing Training Data from GS Artifacts

This doc explains how to prepare a minimal training dataset from Gold-Standard (GS) test artifacts produced by the GS harness.

Usage

Run the helper script which copies selected fields from the GS artifacts into a compact JSON:

```bash
python3 scripts/prepare_training.py --in <artifact_dir> --out training_data
```

By default the script looks for `$HOME/UNIBOT_reports` and `artifacts/*/reports` in the repository.

Output

- `training_data/gs_training.json`: contains `meta` (run summary) and `tests` (list of test entries with `id`, `name`, `time_s`, and `label` where `label`=1 for pass, 0 for fail).

Notes

- This is intentionally minimal; extend it with additional features (stack traces, failure messages, host metadata) for more advanced training.
