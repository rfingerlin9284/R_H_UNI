"""Lightweight dry-run demo harness.

Runs the extractor in a safe, read-only mode and writes logs/artifacts under
the provided output directory.
"""
import argparse
import os
from stochastic import random_hex

from util.logging import get_logger


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="artifacts", help="Output artifacts directory")
    args = p.parse_args()

    run_id = random_hex(8)
    logger = get_logger(run_id=run_id, out_dir=args.out, module="demo_dry_run")

    logger.info("starting dry-run demo", {"run_id": run_id})

    # call extractor and pass run-scoped logger so logs include run_id
    try:
        from wolf_packs.extracted_oanda import calculate_signals

        # give connectors a logger bound to this run
        connector_logger = get_logger(run_id=run_id, out_dir=args.out, module="wolf_packs.extracted_oanda")
        sigs = calculate_signals(logger=connector_logger)
        logger.info("demo signals", {"signals": sigs})
    except Exception as e:
        logger.error("demo failed", {"error": str(e)})

    logger.info("demo finished", {"run_id": run_id})


if __name__ == "__main__":
    main()
