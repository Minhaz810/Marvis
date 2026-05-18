#!/bin/bash
set -e

cd "$(dirname "$0")"
source venv/bin/activate
PYTHONPATH=. python shared/seeds/run_seeds.py
