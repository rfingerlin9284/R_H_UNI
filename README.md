# R_H_UNI
UNIBOT JUST COINBASE AND OANDA

Stochastic-first policy
-----------------------

This project follows a "stochastic-first" policy: randomness is treated as
the default and reproducible (deterministic) runs are only an explicit opt-in
for debugging or auditing. Use the helpers in `stochastic.py` for randomness
and `wolf_packs.stochastic_config.load_thresholds()` to load thresholds with the
standard jitter applied.

Before running live trading, add structured logging and run a dry-run demo to
inspect behavior under realistic variability.

GS test results
---------------

Recent GS (gold-standard) tests were executed locally against `tests/wolf_packs`.
- Tests run: 2
- Passed: 2
- JUnit XML: `artifacts/20250926_041644/reports/gs_junit.xml`
- Log file: `artifacts/20250926_041644/reports/gs_test_log.txt`

To re-run the GS tests locally, see `scripts/run_gs_battery.sh` or run the
`bin/run_gs_tests.sh` helper. Generated artifacts are written under `artifacts/`.
