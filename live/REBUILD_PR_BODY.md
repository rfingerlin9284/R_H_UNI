Rebuild Live System - PR Summary

What
----
This PR introduces a new `live/` template containing:
- `core/rick_charter.py` (PIN-gated enforcement module)
- `strategies/` (proven strategy base and extraction placeholder)
- `risk/position_manager.py` (position sizing template)
- `execution/order_executor.py` (OCO/TTL execution template)
- `tests/gold_standard_suite.py` (gold standard test suite placeholder)
- `main_trading_engine.py` (engine wiring, template)

Why
---
To collect and centralize proven, non-deterministic trading components in a gated branch where they can be reviewed, tested, and promoted after passing the Gold Standard validation.

Security & Safety
-----------------
- All templates are PIN-gated and require PIN `841921` for operational validation.
- `tools/purge_deterministic.py` will run on PRs to surface any deterministic seeds.
- No `live/` files are active in production until human-reviewed and merged.

Next steps
----------
1. Review templates and identify concrete source files for extraction.
2. Run `tools/purge_deterministic.py` and `pytest` in CI (workflow included).
3. Extract strategy logic from proven repos and implement `extracted_profitable_strategy.py`.
4. Complete Gold Standard test implementations and run in CI.
