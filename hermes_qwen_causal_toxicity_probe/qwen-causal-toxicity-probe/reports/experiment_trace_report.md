# Experiment Trace Report

Generated at: 2026-05-23 23:44:30

## Current config.yaml
```yaml
# model_name: Qwen/Qwen2.5-0.5B-Instruct
# max_new_tokens: 256
# do_sample: false
# datasets:
#   - data/generated/toxicity_vignettes.jsonl
#   - data/generated/ablated_vignettes.jsonl
#   - data/generated/renamed_vignettes.jsonl
# prompt_types:
#   - direct
#   - mechanistic
#   - confounding_aware
#   - adversarial
#   - minimal
#   - counterfactual
# output_dir: results
# batch_size: 1
# hidden_states:
#   prompt_type: mechanistic
#   save_mean_pool: true
#   max_examples: null

#----------------------------------------------------

# model_name: Qwen/Qwen2.5-0.5B-Instruct
# max_new_tokens: 64
# do_sample: false
# datasets:
#   - data/generated/toxicity_vignettes.jsonl
# prompt_types:
#   - direct
# output_dir: results

# -----------------------------------------

# model_name: Qwen/Qwen2.5-0.5B-Instruct
# max_new_tokens: 96
# do_sample: false
# datasets:
#   - data/generated/toxicity_vignettes.jsonl
# prompt_types:
#   - direct
#   - mechanistic
#   - confounding_aware
#   - adversarial
# output_dir: results

# ----------------------------------------

# model_name: Qwen/Qwen2.5-0.5B-Instruct
# max_new_tokens: 96
# do_sample: false

# datasets:
#   - data/generated/toxicity_vignettes.jsonl

# prompt_types:
#   - direct
#   - mechanistic
#   - confounding_aware
#   - adversarial

# output_dir: results


# -------------------

# model_name: Qwen/Qwen2.5-0.5B-Instruct
# max_new_tokens: 96
# do_sample: false

# datasets:
#   - data/generated/renamed_vignettes.jsonl

# prompt_types:
#   - direct
#   - mechanistic
#   - confounding_aware
#   - adversarial

# output_dir: results


# ----------------------------

model_name: Qwen/Qwen2.5-0.5B-Instruct
max_new_tokens: 96
do_sample: false

datasets:
  - data/generated/renamed_vignettes.jsonl

prompt_types:
  - direct
  - mechanistic
  - confounding_aware
  - adversarial

output_dir: results
```

## Run-by-run trace

### generations_20260523_212117.jsonl
- File modified: 2026-05-23 21:21:17
- Run prefix: 20260523_212117
- Manifest: missing (legacy run before metadata logging).
- Records: 48
- Unique examples: 48
- Models in file: ['Qwen/Qwen2.5-0.5B-Instruct']
- Prompt types observed: ['direct']
- Task distribution: clean_mediation: 12, confounding: 12, mechanistic_distractor: 12, selection_bias: 12
- Variant distribution: original: 48
- Overall accuracy: 0.5000
- Overall unclear_rate: 0.0000
- Overall concept_recall_rough: 0.5104
- Mean prompt stability score: 1.0000
- Prompt flip rate across examples: 0.0000

Prompt-level summary:

| prompt_type   |   n |   accuracy |   unclear_rate |   concept_recall_rough |
|:--------------|----:|-----------:|---------------:|-----------------------:|
| direct        |  48 |        0.5 |              0 |               0.510417 |

Variant-level summary:

| variant_type   |   n |   accuracy |
|:---------------|----:|-----------:|
| original       |  48 |        0.5 |

### generations_20260523_214241.jsonl
- File modified: 2026-05-23 21:42:41
- Run prefix: 20260523_214241
- Manifest: missing (legacy run before metadata logging).
- Records: 192
- Unique examples: 48
- Models in file: ['Qwen/Qwen2.5-0.5B-Instruct']
- Prompt types observed: ['adversarial', 'confounding_aware', 'direct', 'mechanistic']
- Task distribution: clean_mediation: 48, confounding: 48, mechanistic_distractor: 48, selection_bias: 48
- Variant distribution: original: 192
- Overall accuracy: 0.5312
- Overall unclear_rate: 0.0000
- Overall concept_recall_rough: 0.3333
- Mean prompt stability score: 0.7812
- Prompt flip rate across examples: 0.8750

Prompt-level summary:

| prompt_type       |   n |   accuracy |   unclear_rate |   concept_recall_rough |
|:------------------|----:|-----------:|---------------:|-----------------------:|
| adversarial       |  48 |   0.833333 |              0 |               0.21875  |
| confounding_aware |  48 |   0.5      |              0 |               0.1875   |
| direct            |  48 |   0.5      |              0 |               0.520833 |
| mechanistic       |  48 |   0.291667 |              0 |               0.40625  |

Variant-level summary:

| variant_type   |   n |   accuracy |
|:---------------|----:|-----------:|
| original       | 192 |    0.53125 |

### generations_20260523_231419.jsonl
- File modified: 2026-05-23 23:14:19
- Run prefix: 20260523_231419
- Manifest: missing (legacy run before metadata logging).
- Records: 192
- Unique examples: 48
- Models in file: ['Qwen/Qwen2.5-0.5B-Instruct']
- Prompt types observed: ['adversarial', 'confounding_aware', 'direct', 'mechanistic']
- Task distribution: clean_mediation: 48, confounding: 48, mechanistic_distractor: 48, selection_bias: 48
- Variant distribution: renamed_terms: 192
- Overall accuracy: 0.5052
- Overall unclear_rate: 0.0000
- Overall concept_recall_rough: 0.2917
- Mean prompt stability score: 0.7448
- Prompt flip rate across examples: 1.0000

Prompt-level summary:

| prompt_type       |   n |   accuracy |   unclear_rate |   concept_recall_rough |
|:------------------|----:|-----------:|---------------:|-----------------------:|
| adversarial       |  48 |   0.75     |              0 |              0.21875   |
| confounding_aware |  48 |   0.5      |              0 |              0.0833333 |
| direct            |  48 |   0.520833 |              0 |              0.40625   |
| mechanistic       |  48 |   0.25     |              0 |              0.458333  |

Variant-level summary:

| variant_type   |   n |   accuracy |
|:---------------|----:|-----------:|
| renamed_terms  | 192 |   0.505208 |

### generations_20260523_232437.jsonl
- File modified: 2026-05-23 23:24:37
- Run prefix: 20260523_232437
- Manifest: missing (legacy run before metadata logging).
- Records: 192
- Unique examples: 48
- Models in file: ['Qwen/Qwen2.5-0.5B-Instruct']
- Prompt types observed: ['adversarial', 'confounding_aware', 'direct', 'mechanistic']
- Task distribution: clean_mediation: 48, confounding: 48, mechanistic_distractor: 48, selection_bias: 48
- Variant distribution: renamed_terms: 192
- Overall accuracy: 0.5052
- Overall unclear_rate: 0.0000
- Overall concept_recall_rough: 0.2917
- Mean prompt stability score: 0.7448
- Prompt flip rate across examples: 1.0000

Prompt-level summary:

| prompt_type       |   n |   accuracy |   unclear_rate |   concept_recall_rough |
|:------------------|----:|-----------:|---------------:|-----------------------:|
| adversarial       |  48 |   0.75     |              0 |              0.21875   |
| confounding_aware |  48 |   0.5      |              0 |              0.0833333 |
| direct            |  48 |   0.520833 |              0 |              0.40625   |
| mechanistic       |  48 |   0.25     |              0 |              0.458333  |

Variant-level summary:

| variant_type   |   n |   accuracy |
|:---------------|----:|-----------:|
| renamed_terms  | 192 |   0.505208 |

## Cross-run change trace

| run_file | run_prefix | run_name | modified_time | n_records | unique_examples | models | prompt_types | manifest |
|---|---|---|---:|---:|---:|---|---|---|
| generations_20260523_212117.jsonl | 20260523_212117 | legacy | 2026-05-23 21:21:17 | 48 | 48 | Qwen/Qwen2.5-0.5B-Instruct | direct | no |
| generations_20260523_214241.jsonl | 20260523_214241 | legacy | 2026-05-23 21:42:41 | 192 | 48 | Qwen/Qwen2.5-0.5B-Instruct | adversarial;confounding_aware;direct;mechanistic | no |
| generations_20260523_231419.jsonl | 20260523_231419 | legacy | 2026-05-23 23:14:19 | 192 | 48 | Qwen/Qwen2.5-0.5B-Instruct | adversarial;confounding_aware;direct;mechanistic | no |
| generations_20260523_232437.jsonl | 20260523_232437 | legacy | 2026-05-23 23:24:37 | 192 | 48 | Qwen/Qwen2.5-0.5B-Instruct | adversarial;confounding_aware;direct;mechanistic | no |

## Traceability status
- New runs now support exact per-run YAML snapshots and machine-readable manifests under results/metadata/.
- Legacy runs (before this update) are still inferential unless their YAML was manually preserved elsewhere.
