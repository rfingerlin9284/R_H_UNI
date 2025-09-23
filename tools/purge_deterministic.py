#!/usr/bin/env python3
"""Scan and optionally purge deterministic-seed patterns from a codebase.

This tool runs in dry-run mode by default and reports occurrences of common
deterministic patterns (np.random.seed, random.seed, PYTHONHASHSEED, hardcoded
seed values, and obvious counter-based deterministic logic like 'entry_counter').

Usage:
  python tools/purge_deterministic.py --dry-run
  python tools/purge_deterministic.py --apply  # applies safe edits with backups

Edits are conservative: the default replacement comments the line and inserts
an audit note. Files are backed up to `./.state/purge_backups/` before edits.
"""
from __future__ import annotations
import re
import sys
import argparse
from pathlib import Path
import json
import shutil

RE_POISONS = [
    r"np\.random\.seed\s*\(",
    r"random\.seed\s*\(",
    r"PYTHONHASHSEED",
    r"seed=\s*\d+",
    r"entry_counter\b",
    r"%\s*3\s*==\s*0",  # suspicious counter mod patterns
]

IGNORED_DIRS = {".git", "node_modules", "venv", ".venv", "bot_minimal", "__pycache__", ".state"}


def is_ignored(path: Path) -> bool:
    for p in path.parts:
        if p in IGNORED_DIRS:
            return True
    return False


def find_poison_lines(path: Path):
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []
    findings = []
    for i, line in enumerate(text.splitlines(), start=1):
        for pat in RE_POISONS:
            if re.search(pat, line):
                findings.append({"line_no": i, "line": line.rstrip("\n"), "pattern": pat})
                break
    return findings


def scan_repo(root: Path):
    results = {}
    for p in root.rglob("*.py"):
        if is_ignored(p):
            continue
        rel = p.relative_to(root)
        findings = find_poison_lines(p)
        if findings:
            results[str(rel)] = findings
    return results


def backup_file(root: Path, f: Path, backup_root: Path):
    dest = backup_root / f.relative_to(root)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(f, dest)


def apply_fixes(root: Path, findings: dict, backup_root: Path):
    # Conservative fix: comment the offending line and add an audit note
    for rel_path, entries in findings.items():
        fpath = root / rel_path
        backup_file(root, fpath, backup_root)
        text = fpath.read_text(encoding="utf-8")
        lines = text.splitlines()
        for e in entries[::-1]:
            i = e["line_no"] - 1
            old = lines[i]
            comment = f"# PURGED_DETERMINISTIC: original: {old.strip()}  # consult audit"
            lines[i] = comment
        fpath.write_text("\n".join(lines), encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Apply conservative edits (requires backup).")
    parser.add_argument("--root", default=".", help="Repository root to scan")
    parser.add_argument("--out", default=".state/deterministic_findings.json", help="Output JSON for findings")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    findings = scan_repo(root)
    out.write_text(json.dumps(findings, indent=2), encoding="utf-8")
    print(f"Found {len(findings)} files with deterministic patterns. Report: {out}")

    if args.apply:
        backup_root = Path('.state') / 'purge_backups'
        backup_root.mkdir(parents=True, exist_ok=True)
        apply_fixes(root, findings, backup_root)
        print(f"Applied conservative fixes. Backups at: {backup_root}")


if __name__ == '__main__':
    main()
