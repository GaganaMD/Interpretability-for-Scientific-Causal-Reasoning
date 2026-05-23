#!/usr/bin/env bash
set -euo pipefail

python src/generate_dataset.py
python src/validate_dataset.py
python src/run_generation.py
python src/score_outputs.py
python src/analyze_prompt_sensitivity.py
