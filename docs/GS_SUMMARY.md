# Gold-Standard (GS) quick summary

Artifacts location: `/home/ing/UNIBOT_reports`

- Tests run: `pytest tests/wolf_packs` (minimal smoke tests)
- Results: 2 passed, 0 failed
- JUnit XML: `/home/ing/UNIBOT_reports/gs_junit.xml`
- Parsed outputs: `/home/ing/UNIBOT_reports/gs_test_matrix.json`, `/home/ing/UNIBOT_reports/run_summary.json`

How to re-run locally (recommended):

```bash
cd /home/ing/RICK/R_H_UNI
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./scripts/run_gs_battery.sh
deactivate
```
