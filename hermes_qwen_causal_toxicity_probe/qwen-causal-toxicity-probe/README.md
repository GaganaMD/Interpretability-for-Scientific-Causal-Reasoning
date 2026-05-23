# Qwen2.5 Causal Toxicity Reasoning Probe

## Goal
Build a runnable, modular, laptop-first interpretability prototype for studying prompt-conditioned behavior and representation shifts in Qwen2.5 models on synthetic causal-toxicity reasoning tasks.

## Scientific scope and caution
- All vignettes are synthetic methodological artifacts, not biomedical facts.
- Behavioral scores, probe metrics, and activation similarities are exploratory correlational signals.
- Probe separability does not prove the model uses a concept causally during generation.
- Representation similarity or drift does not prove mechanistic causal abstraction.

## Why Qwen2.5 for this scaffold
- Open checkpoints and local execution.
- Direct access to hidden states and logits through HuggingFace Transformers + PyTorch.
- Repeatable prompt/variant contrast workflows that are difficult in closed API-only settings.

## Repository structure
- `src/generate_dataset.py`: synthetic vignette generation (original + ablated + renamed variants)
- `src/validate_dataset.py`: schema/field checks and distribution summaries
- `src/run_generation.py`: local chat-template inference across prompt types
- `src/score_outputs.py`: yes/no parsing + rough concept mention scoring
- `src/analyze_prompt_sensitivity.py`: prompt answer stability and flip analysis
- `src/collect_hidden_states.py`: selective hidden-state collection without generation
- `src/train_probe.py`: layerwise linear probes (logistic regression)
- `src/analyze_activation_contrasts.py`: original-vs-variant layerwise cosine distances
- `src/analyze_representation_stability.py`: prompt-pair latent drift analysis
- `src/generate_experiment_report.py`: run manifest + YAML-snapshot experiment tracking report

## Dataset design
Task families:
- `clean_mediation`
- `confounding`
- `selection_bias`
- `mechanistic_distractor`

Variant families:
- Causally relevant perturbations: `confounder_removed`, `mediator_removed`, `randomized_design`, `selection_bias_added`
- Terminology perturbation: `renamed_terms` (biomedical terms -> neutral variables)

This setup supports testing invariance under wording changes vs sensitivity under causal graph changes.

## Prompt contrast experiments
Prompt types:
- `direct`
- `mechanistic`
- `confounding_aware`
- `adversarial`
- `minimal`
- `counterfactual`

## Hidden-state and representation analysis
`collect_hidden_states.py` supports:
- one or multiple prompt types
- optional `max_examples` bounding for laptop runs
- per-layer final-token vectors
- optional per-layer mean-pooled vectors

Analyses:
- `analyze_activation_contrasts.py`: compares original vs variant representations by `pair_id`
- `analyze_representation_stability.py`: compares baseline prompt representations vs alternate prompts for the same example (`prompt latent drift`)

## Experiment tracking (YAML differentiation)
Recommended workflow:
1. Create one YAML per experiment in `configs/experiments/`
2. Run with label:
   `python src/run_generation.py --config configs/experiments/exp_001.yaml --run_name exp_001`

Saved per run:
- `results/generations/generations_<timestamp>_<run_name>.jsonl`
- `results/metadata/config_<timestamp>_<run_name>.yaml`
- `results/metadata/run_manifest_<timestamp>_<run_name>.json`

Consolidated report:
- `python src/generate_experiment_report.py`
- output: `reports/experiment_trace_report.md`

## Quick start
1) Environment
- `python -m venv .venv`
- `source .venv/Scripts/activate` (Git-Bash on Windows)
- `pip install -r requirements.txt`

2) Data sanity
- `python src/generate_dataset.py`
- `python src/validate_dataset.py`

3) Behavioral pipeline (model required)
- `bash scripts/run_small_pilot.sh`

4) Hidden-state pipeline (model required)
- `bash scripts/run_hidden_state_demo.sh`

## Expected outputs
- `results/generations/*.jsonl`
- `results/scores/scored_generations.csv`
- `results/scores/summary_by_task_and_prompt.csv`
- `results/scores/prompt_stability.csv`
- `results/activations/qwen2p5_hidden_states.pt`
- `results/scores/probe_by_layer.csv`
- `results/scores/activation_contrasts.csv`
- `results/scores/prompt_latent_drift.csv`
- `results/scores/prompt_latent_drift_summary.csv`

## Research documentation (core artifacts)
- `docs/research_evolution.md`: deep scientific narrative of project evolution and emerging hypotheses.
- `docs/interpretability_reporting_standard.md`: required interpretation sections for future experiment artifacts.
- `reports/experiment_trace_report.md`: run-level trace + auto-generated interpretability commentary.

## Laptop-first assumptions and limits
- Default model: `Qwen/Qwen2.5-0.5B-Instruct`
- CPU is supported, but hidden-state collection can still be slow.
- Larger checkpoints (1.5B/7B) require materially more RAM/VRAM.
- First run requires model download from HuggingFace.
