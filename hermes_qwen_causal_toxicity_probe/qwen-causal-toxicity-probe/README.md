# Qwen2.5 Causal Toxicity Reasoning Probe

## Goal
Build an implementation-first, laptop-friendly research scaffold to study whether Qwen2.5 behavior on synthetic toxicity vignettes is stable under prompt changes and causal-structure perturbations.

## Motivation
Causal-sounding outputs can arise from surface cues, framing effects, or biologically flavored distractors. This repo provides controlled synthetic tasks and lightweight analyses to inspect that risk.

## Why Qwen2.5?
- Open checkpoints and local inference.
- Hidden states are inspectable.
- Prompt contrast and activation analyses are reproducible.
- These workflows are often not possible in closed API-only settings.

## Dataset design
Synthetic vignettes (not medical claims) with task types:
- clean_mediation
- confounding
- selection_bias
- mechanistic_distractor

Each example contains structured fields (exposure, initiating event, mediator, outcome, bias variable, study design), a causal question, and synthetic gold labels.

Variants:
- Ablations: confounder_removed, mediator_removed, randomized_design, selection_bias_added
- Renaming: biomedical terms mapped to neutral variables

## Prompt contrast experiments
Prompt families: direct, mechanistic, confounding-aware, adversarial, minimal, counterfactual.
Run all prompt types on all examples and measure answer stability + concept mention recall.

## Faithfulness and causal ablation tests
Original vs ablated/renamed variants allow behavior and activation comparisons under graph-relevant and wording-only changes.

## Hidden-state extraction
Forward-pass-only activation collection (no generation) saves per-layer final-token and mean-pooled representations.

## Representation probing
Layerwise logistic probes test linear recoverability for:
- confounding present
- mediation present
- selection_bias present

Important caution: probe performance indicates recoverability, not proof that the model causally uses that information.

## How to run
1) Install dependencies
- `python -m venv .venv`
- `source .venv/Scripts/activate` (Git-Bash on Windows)
- `pip install -r requirements.txt`

2) Generate + validate datasets
- `python src/generate_dataset.py`
- `python src/validate_dataset.py`

3) Full small pilot (requires model download)
- `bash scripts/run_small_pilot.sh`

4) Hidden-state demo (requires model download)
- `bash scripts/run_hidden_state_demo.sh`

## Experiment tracking and YAML differentiation
Use one YAML per experiment and run with a run label:
- `python src/run_generation.py --config configs/experiments/exp_001.yaml --run_name exp_001`

For each run, the pipeline now saves:
- `results/generations/generations_<timestamp>_<run_name>.jsonl`
- `results/metadata/config_<timestamp>_<run_name>.yaml` (exact snapshot used)
- `results/metadata/run_manifest_<timestamp>_<run_name>.json`

Generate the consolidated report:
- `python src/generate_experiment_report.py`

Report output:
- `reports/experiment_trace_report.md`

## Expected outputs
- `results/generations/generations_<timestamp>.jsonl`
- `results/scores/scored_generations.csv`
- `results/scores/summary_by_task_and_prompt.csv`
- `results/scores/prompt_stability.csv`
- `results/activations/qwen2p5_hidden_states.pt`
- `results/scores/probe_by_layer.csv`
- `results/scores/activation_contrasts.csv`

## Limitations
- Synthetic benchmark only.
- Keyword scoring is rough.
- Probe interpretation is limited.
- No medical claims.
- No proof of internal causal mechanisms.

## Application relevance
Useful as an early-stage interpretability workflow for iterative experimentation on limited local compute.

## Scientific caution statement
This project does not claim to prove mechanistic interpretability. It is an experimental scaffold for behavioral and representation-level analysis.
