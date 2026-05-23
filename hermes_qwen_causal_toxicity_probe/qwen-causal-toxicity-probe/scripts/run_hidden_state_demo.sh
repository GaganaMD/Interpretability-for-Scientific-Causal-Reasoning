#!/usr/bin/env bash
set -euo pipefail

python src/collect_hidden_states.py
python src/train_probe.py
python src/analyze_activation_contrasts.py
