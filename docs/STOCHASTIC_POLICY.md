Project stochastic-first policy
===============================

This repository enforces a "stochastic-first" policy: by default, code should not rely on fixed random seeds, hard-coded RNG values, or deterministic behavior. Real markets and production systems are inherently non-deterministic; deterministic logic must be an explicit opt-in used only for debugging or auditing.

How this is enforced in the repo
-- All randomness should use `stochastic.py` helpers.
-- The project defaults to non-deterministic entropy; deterministic runs are an explicit opt-in for debugging and auditing only.

Run identifiers are generated nondeterministically by the tooling and should not be treated as environment-controlled labels.

Why this matters
- Avoids accidental overfitting and helps tests better reflect production variability.
- Ensures the bot's behavior more closely matches live market unpredictability.

Deterministic runs are no longer supported by the project. For reproducible debugging you should instead capture and record runtime artifacts (logs, inputs, outputs) and use those for analysis.

Do not modify this policy file except to update guidance or to expand the helper API in `stochastic.py`.
