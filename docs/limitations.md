# Limitations

## Synthetic data constraints
- Vignettes are synthetic and simplified.
- Label quality reflects designed structure, not real-world biomedical truth.
- Distributional realism is limited.

## Prompt and parsing constraints
- Yes/no parsing is intentionally simple and can misread nuanced responses.
- Concept mention scoring is keyword-based and approximate.

## Representation-analysis constraints
- Cosine similarity/distance captures geometric shifts, not semantic certainty.
- Layerwise drift does not by itself identify causal mechanisms.
- Pooled representations may hide token-level details.

## Probe interpretation constraints
- Linear probes measure recoverability, not necessity.
- High probe accuracy does not prove causal use during reasoning.

## Compute constraints
- Laptop-first defaults require bounded sample counts and selective collection.
- CPU runs can be slow; larger checkpoints may be impractical locally.

## Safety and epistemic constraints
- No medical advice or biomedical factual claims should be inferred.
- This repository is an exploratory research scaffold, not proof of mechanistic interpretability.
