# Chat Addendums & Charter

This file collects recent addendums, decisions, and the project's stochastic-first charter derived from interactive edits.

---

## Latest addendum (timestamped 2025-09-25)

PROCEED WITH 1

Acknowledged: proceed to propagate the run-scoped logger into connectors and run the demo to verify run_id propagation. Actions taken:

- Added `util/logging.py` — JSON structured logger writing to stdout and `artifacts/<run_id>/logs.jsonl`.
- Added `util/retry.py` — retry decorator with exponential backoff + jitter.
- Edited `wolf_packs/extracted_oanda.py` to accept an optional `logger` and use it for connector logs.
- Edited `scripts/demo_dry_run.py` to create a `run_id`, create a run-scoped logger, and pass that logger to the connector.
- Ran demo: `PYTHONPATH=. python3 scripts/demo_dry_run.py --out artifacts` -> generated artifacts and logs showing `run_id` in connector logs.

Tests: all unit tests passed after changes (4 passed).

---

## Stochastic-first policy (short)

By default, code should not rely on fixed random seeds or deterministic behavior. Use `stochastic.py` helpers for randomness and `wolf_packs.stochastic_config.load_thresholds()` to load thresholds with jitter.

Deterministic runs are only an opt-in for debugging/auditing; the project prefers recording artifacts (logs, inputs, outputs) to reproduce runs.

---

# Addendum: Logical Path Confirmation and Task Progress Tracking

## Logical Path Confirmation
This addendum introduces a structured approach to confirm the next logical steps and provide options for subsequent tasks. The assistant will:

1. Summarize the current state of the system or task.
2. Propose the next logical steps based on the current context.
3. Offer a set of options for the user to choose from for the next task.
4. Confirm the selected option before proceeding.

## Task Progress Tracking
To ensure clarity on the state of the system, the assistant will maintain a structured to-do list that includes:

1. **Task Name**: A brief description of the task.
2. **Completion Percentage**: An estimate of how much of the task is complete.
3. **Pending Actions**: Specific actions or subtasks that still need attention.

### Example To-Do List Format

| Task Name                  | Completion Percentage | Pending Actions                       |
|----------------------------|-----------------------|---------------------------------------|
| Create `run_gs_tests.sh`   | 100%                  | None                                  |
| Execute GS tests           | 100%                  | None                                  |
| Resolve `pytest` dependency| 100%                  | None                                  |
| Review test results        | 100%                  | None                                  |
| Update documentation       | 0%                    | Add test results summary to README.md|

This structured approach will help the user track progress and prioritize tasks effectively.

---

## Comprehensive Project Punch List

### Overall Project Completion
| Task Name                          | Completion Percentage | Pending Actions                                      |
|------------------------------------|-----------------------|----------------------------------------------------|
| Create `run_gs_tests.sh`           | 100%                  | None                                               |
| Execute GS tests                   | 100%                  | None                                               |
| Resolve `pytest` dependency        | 100%                  | None                                               |
| Review test results                | 100%                  | None                                               |
| Update documentation               | 0%                    | Add test results summary to README.md             |
| Implement stochastic-first policy  | 80%                   | Ensure all randomness uses `stochastic.py` helpers|
| Verify live readiness toggling     | 100%                  | None                                               |
| Add unit tests for retry decorator | 0%                    | Write tests for `util/retry.py`                   |
| Audit CI pipeline                  | 50%                   | Ensure no deterministic env vars are used         |
| Generate final reports             | 0%                    | Run `generate_report.sh` and verify outputs       |

### Live Version Training and Verification
| Task Name                          | Completion Percentage | Pending Actions                                      |
|------------------------------------|-----------------------|----------------------------------------------------|
| Train system with GS artifacts     | 0%                    | Use `gs_runner.py` outputs for training           |
| Verify stochastic thresholds       | 50%                   | Test `load_thresholds()` under various scenarios  |
| Validate orchestrator behavior     | 50%                   | Add tests for `orchestrator.py`                   |
| Finalize live trading configs      | 0%                    | Review and update `configs/wolfpack_config.json`  |
| Conduct dry-run demo               | 100%                  | None                                               |

This punch list provides a clear view of the project's progress and highlights areas that need attention. Let me know if you need further refinements.

---

## Next suggested actions

1. Propagate the run-scoped logger across the orchestrator to ensure every component includes `run_id` in logs.
2. Add unit tests for `util/retry.py` and for logger run_id persistence.
3. Audit CI and docs to ensure no deterministic env vars are re-introduced.

---

If you'd like this file to capture every chat message going forward, say "enable chat logging" and I'll append subsequent addenda automatically.

### Current chat-logging status

- enabled: true
- mode: summary
- auto_append: true
- redact: false
