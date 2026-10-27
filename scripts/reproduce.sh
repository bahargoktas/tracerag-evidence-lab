#!/usr/bin/env bash
set -euo pipefail
python -m pip install -e '.[dev]'
python -m tracerag.cli check-data
pytest -q
python -m tracerag.cli tune
python -m tracerag.cli evaluate --split test --out reports
python -m tracerag.cli evaluate --split challenge --out reports/challenge
