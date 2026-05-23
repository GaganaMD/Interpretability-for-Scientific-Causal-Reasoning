# Experimental design

## Research objective
Assess whether Qwen2.5 outputs and latent representations are stable under prompt reframing and terminology perturbations, while remaining sensitive to causally relevant structure edits.

## Benchmark categories
1. clean_mediation
2. confounding
3. selection_bias
4. mechanistic_distractor

## Synthetic vignette schema
Each item includes structured causal fields (exposure, initiating event, mediator, outcome, bias variable, study design), natural-language vignette text, question, and synthetic labels.

## Perturbation families
- Graph-relevant edits: confounder removal, mediator removal, randomized design, selection bias addition.
- Surface-form edits: renamed terms (biomedical tokens to neutral variables).
- Prompt reframing: direct, mechanistic, confounding-aware, adversarial, minimal, counterfactual.

## Behavioral metrics
- Prompt-conditioned answer accuracy (synthetic labels)
- Unclear answer rate
- Rough concept mention recall
- Prompt stability score / answer flips across prompts

## Representation metrics
- Layerwise cosine distance between original vs perturbed variants (same prompt)
- Prompt-pair latent drift per example (same item, different prompt)
- Optional mean-pooled representation contrasts alongside final-token contrasts

## Why simple accuracy is insufficient
A model can be accurate on average while:
- being highly unstable across prompt wording,
- shifting strongly under terminology changes,
- relying on superficial cues not aligned with intended causal structure.

This scaffold therefore combines behavior and latent-space contrasts.
