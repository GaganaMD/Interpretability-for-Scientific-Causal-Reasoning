# Qwen2.5 Causal Toxicity Reasoning Probe

## Goal

Build a runnable, modular, laptop-first interpretability prototype for studying prompt-conditioned behavior and latent representation shifts in Qwen2.5 models on synthetic causal-toxicity reasoning tasks.

This repository is intentionally designed for small-scale, reproducible interpretability experimentation on consumer hardware using open-source local models and lightweight analysis workflows.

---

## Research motivation

Large language models can exhibit substantial behavioral changes under prompt reframing even when the underlying causal structure of a task remains fixed. This project investigates whether such behavioral instability corresponds to measurable latent representation drift inside small open Qwen2.5 models under causal confounding, mediation, terminology perturbation, and prompt reframing conditions.

The project evolved from a behavioral prompt-sensitivity benchmark into a lightweight mechanistic interpretability experimentation framework focused on:

* prompt-conditioned reasoning instability,
* latent representation drift,
* causal abstraction robustness,
* and representation stability under controlled perturbations.

---

## Scientific scope and caution

* All vignettes are synthetic methodological artifacts, not biomedical facts.
* Behavioral scores, probe metrics, and activation similarities are exploratory correlational signals.
* Probe separability does not prove the model uses a concept causally during generation.
* Representation similarity or drift does not prove mechanistic causal abstraction.
* Hidden-state movement does not establish internal causal mechanisms.
* Synthetic toxicity performance should not be interpreted as biomedical competence.

This repository is intended as a lightweight exploratory interpretability environment rather than a mechanism-proof framework.

---

## Why Qwen2.5 for this scaffold

* Open checkpoints and local execution.
* Direct access to hidden states and logits through HuggingFace Transformers + PyTorch.
* Repeatable prompt/variant contrast workflows that are difficult in closed API-only settings.
* Lightweight enough for laptop-scale experimentation while still exhibiting nontrivial reasoning instability.

---

## Early experimental observations

Initial experiments using `Qwen/Qwen2.5-0.5B-Instruct` showed:

* strong prompt-conditioned behavioral instability under fixed causal structure,
* high answer flip rates across prompt reframings,
* mechanistic prompts produced the largest latent representation drift and lowest behavioral accuracy,
* renamed terminology variants further reduced prompt stability,
* measurable but moderate latent drift across prompt families,
* and drift concentration in early/mid selected layers during bounded hidden-state runs.

These findings are exploratory and based on synthetic datasets with limited sample counts. They should not be interpreted as evidence of genuine causal abstraction or mechanistic reasoning failure.

---

## Current project status

### Implemented

* synthetic benchmark generation
* multi-prompt behavioral evaluation
* prompt stability and flip analysis
* hidden-state extraction
* prompt-conditioned latent drift analysis
* activation contrast analysis
* lightweight layerwise probing workflows
* experiment trace reporting
* YAML-based experiment reproducibility tracking

### In progress

* behavioral-flip vs latent-drift correlation analysis
* denser layerwise latent sweeps
* pooling-strategy comparisons
* cross-model scaling experiments
* uncertainty estimation and bootstrap confidence intervals

---

## Repository structure

* `src/generate_dataset.py`

  * synthetic vignette generation (original + ablated + renamed variants)

* `src/validate_dataset.py`

  * schema checks and distribution summaries

* `src/run_generation.py`

  * local chat-template inference across prompt types

* `src/score_outputs.py`

  * yes/no parsing and rough concept mention scoring

* `src/analyze_prompt_sensitivity.py`

  * prompt answer stability and flip analysis

* `src/collect_hidden_states.py`

  * selective hidden-state collection without generation

* `src/train_probe.py`

  * lightweight layerwise linear probes using logistic regression

* `src/analyze_activation_contrasts.py`

  * original-vs-variant layerwise cosine distance analysis

* `src/analyze_representation_stability.py`

  * prompt-pair latent drift analysis

* `src/run_latent_experiment.py`

  * orchestrated latent representation experiment pipeline

* `src/generate_experiment_report.py`

  * run manifest and YAML-snapshot experiment tracking report generation

---

## Dataset design

### Task families

* `clean_mediation`
* `confounding`
* `selection_bias`
* `mechanistic_distractor`

### Variant families

#### Causally relevant perturbations

* `confounder_removed`
* `mediator_removed`
* `randomized_design`
* `selection_bias_added`

#### Terminology perturbation

* `renamed_terms`

  * biomedical terms replaced with neutral variables

This setup supports testing:

* invariance under wording changes,
* sensitivity under causal graph changes,
* and prompt-conditioned reasoning robustness.

---

## Prompt contrast experiments

### Prompt families

* `direct`
* `mechanistic`
* `confounding_aware`
* `adversarial`
* `minimal`
* `counterfactual`

The benchmark is designed to test whether reasoning behavior and latent representations remain stable under:

* framing changes,
* instruction density shifts,
* mechanistic prompting,
* and adversarial reframing.

---

## Hidden-state and representation analysis

`collect_hidden_states.py` supports:

* one or multiple prompt types,
* optional `max_examples` bounds for laptop runs,
* selective layer extraction,
* per-layer final-token vectors,
* optional mean-pooled vectors,
* optional max-pooled vectors,
* and prompt-conditioned activation collection.

### Representation analyses

#### `analyze_activation_contrasts.py`

Compares:

* original vs perturbed variants,
* confounder removals,
* mediator removals,
* randomized designs,
* and selection-bias perturbations

using layerwise cosine distances.

#### `analyze_representation_stability.py`

Measures:

* prompt-conditioned latent drift,
* cross-prompt representation similarity,
* within-example representation consistency,
* and baseline-vs-variant representation movement.

---

## Experiment tracking and reproducibility

### Recommended workflow

1. Create one YAML per experiment:

```bash
configs/experiments/exp_001.yaml
```

2. Run labeled experiments:

```bash
python src/run_generation.py --config configs/experiments/exp_001.yaml --run_name exp_001
```

### Saved per run

* `results/generations/generations_<timestamp>_<run_name>.jsonl`
* `results/metadata/config_<timestamp>_<run_name>.yaml`
* `results/metadata/run_manifest_<timestamp>_<run_name>.json`

### Consolidated reporting

```bash
python src/generate_experiment_report.py
```

Output:

```bash
reports/experiment_trace_report.md
```

The reporting system automatically tracks:

* prompt families,
* variants,
* metrics,
* run metadata,
* and interpretability commentary.

---

## Quick start

### 1. Environment setup

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

### 2. Dataset sanity checks

```bash
python src/generate_dataset.py
python src/validate_dataset.py
```

### 3. Behavioral pipeline

```bash
bash scripts/run_small_pilot.sh
```

### 4. Hidden-state pipeline

```bash
bash scripts/run_hidden_state_demo.sh
```

### 5. Full latent representation experiment

```bash
python src/run_latent_experiment.py --config config.yaml --run_name latent_real_phase1 --max_examples 52 --layers 0:25:4
```

---

## Expected outputs

### Behavioral artifacts

* `results/generations/*.jsonl`
* `results/scores/scored_generations.csv`
* `results/scores/summary_by_task_and_prompt.csv`
* `results/scores/prompt_stability.csv`

### Hidden-state artifacts

* `results/activations/qwen2p5_hidden_states.pt`

### Representation analysis outputs

* `results/scores/probe_by_layer.csv`
* `results/scores/activation_contrasts.csv`
* `results/scores/activation_contrasts_summary.csv`
* `results/scores/prompt_latent_drift.csv`
* `results/scores/prompt_latent_drift_summary.csv`
* `results/scores/prompt_within_example_consistency.csv`

### Reports

* `reports/experiment_trace_report.md`
* `reports/latent_representation_report_*.md`

---

## Research documentation

### Core artifacts

* `docs/research_evolution.md`

  * scientific narrative of project evolution and emerging hypotheses

* `docs/interpretability_reporting_standard.md`

  * standardized interpretability reporting structure

* `docs/latent_phase_methodology.md`

  * latent representation analysis methodology and assumptions

* `reports/experiment_trace_report.md`

  * run-level trace with auto-generated interpretability commentary

---

## Typical hardware profile

Tested on:

* RTX 3060 Laptop GPU (6GB VRAM)
* CUDA-enabled PyTorch
* CPU-compatible fallback workflows

Recommended for laptop-scale hidden-state experiments:

* selective layer extraction,
* bounded sample counts,
* and small batch sizes.

---

## Laptop-first assumptions and limitations

* Default model:

  * `Qwen/Qwen2.5-0.5B-Instruct`

* CPU execution is supported, though hidden-state collection may still be slow.

* Larger checkpoints (`1.5B`, `7B`) require materially more RAM/VRAM.

* First run requires downloading model weights from HuggingFace.

* Current experiments intentionally avoid:

  * full activation dumps,
  * exhaustive token-level tracing,
  * distributed infrastructure,
  * and large-scale mechanistic intervention methods.

---

## Non-goals

This project is not intended to:

* establish mechanistic proofs of reasoning,
* recover true internal causal graphs,
* evaluate biomedical competence,
* replace causal tracing or intervention-based interpretability methods,
* or demonstrate faithful chain-of-thought reasoning.

The repository is designed as a lightweight exploratory framework for studying prompt-conditioned representation behavior.

---

## Future directions

Planned extensions include:

* behavioral-flip vs latent-drift correlation studies,
* denser layerwise latent analysis,
* cross-model scaling comparisons,
* prompt-family geometry analysis,
* probe transfer robustness experiments,
* uncertainty estimation and bootstrap confidence intervals,
* and controlled decomposition of terminology perturbation vs instruction-style perturbation effects.

---

## Citation and attribution

This repository was developed as an exploratory interpretability research scaffold focused on:

* causal reasoning robustness,
* prompt-conditioned representation instability,
* and lightweight latent analysis workflows for small open language models.

Please interpret all findings cautiously and avoid overstating mechanistic conclusions from behavioral or representational similarity metrics alone.
