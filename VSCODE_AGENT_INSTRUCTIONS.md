# VSCode Agent Task: Wolf Pack Strategy Assembly

## Goal
Provide instructions for a local VS Code agent to search the filesystem (local + WSL), find candidate strategy files, extract the top 4-5 synergistic methods, and assemble three regime-specialized "wolf pack" strategy modules for Bullish, Bearish, and Sideways markets. The agent must obey the RICK charter constraints and never run or deploy live trading code.

## Safety & sweep rules
- Do not modify or push any live/production branches or files under `live/`.
- Do not exfiltrate secrets; skip files matching `*.env`, `.secrets`, or `credentials` patterns.
- Always run in a sandboxed workspace and present results for human review.

## Steps for the agent
1. Index strategy files found under common locations (`src/`, `*/strategies/`, `~/projects/**/src/**/strategies/`, `/mnt/wsl*/**/src/**/strategies/`).
2. For each file, attempt to import it in a temporary isolated venv and run its test harness if present. Capture metrics (profit, max drawdown, Sharpe) if available in metadata or historical test outputs.
3. Rank candidate strategies by profitability and risk-adjusted return.
4. Extract the top 4-5 methods from high-performing strategies (for example `generate_signals`, `calculate_indicators`, `position_sizing`, `should_exit`, `manage_risk`) and assemble them into three templates specialized by regime.
5. Save assembled modules to `wolf_packs/` inside the repo and copy final artifacts to `~/Desktop` for review.
6. Create a short report `wolf_packs/report.md` documenting the source files used, metrics, and why each method was included.

## Human review and gating
- Always open a PR or present a patch for human review before any push.
- Require PIN 841921 for any commit that touches `live/` or changes the RICK charter.

## Run example (manual)
```bash
# create a sandbox venv and run the agent script locally
python3 -m venv .venv_agent && . .venv_agent/bin/activate
pip install -r requirements-dev.txt
python tools/agent_wolfpack_builder.py --search-paths "/home/ing /mnt/wsl" --out-dir wolf_packs
deactivate
```
