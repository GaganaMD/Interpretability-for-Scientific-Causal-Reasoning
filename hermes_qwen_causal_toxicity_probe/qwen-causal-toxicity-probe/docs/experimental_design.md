# Experimental design

This project uses synthetic causal-toxicity vignettes for controlled methodological experiments.

- Benchmark categories: clean mediation, confounding, selection bias, mechanistic distractor.
- Structure: each vignette encodes exposure, initiating event, mediator, outcome, and possible bias variable.
- Prompt types: direct, mechanistic, confounding-aware, adversarial framing, minimal, and counterfactual.
- Invariance test: renamed biomedical terms into neutral variable names.
- Sensitivity test: ablated graph-relevant information (confounder/mediator/randomization/selection changes).
- Why accuracy is insufficient: prompt-dependent flips and representation shifts can occur despite similar aggregate accuracy.

Interpretation should remain cautious: these are synthetic signals useful for stress-testing behavioral and representational consistency.
