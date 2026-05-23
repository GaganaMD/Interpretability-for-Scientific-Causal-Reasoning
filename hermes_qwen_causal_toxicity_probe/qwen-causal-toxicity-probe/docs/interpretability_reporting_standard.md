# Interpretability Reporting Standard (Project-Wide)

## Purpose
This standard makes interpretability commentary mandatory in all substantial experiment artifacts. Reports must not remain metric-only logs.

## Required sections for every major experiment report
1) Experimental meaning
- What changed relative to prior runs?
- Why does that change matter for interpretability hypotheses?

2) Mechanistic interpretation (tentative)
- Which hypotheses are supported, weakened, or newly introduced?
- Separate observations from inferences.

3) Behavioral vs representation distinction
- Explicitly state whether findings are behavioral-only, representation-only, or both.
- Avoid conflating output flips with latent mechanism changes.

4) Limitations and confounders
- Scoring/parsing caveats
- Dataset/scale constraints
- Prompt/template-induced artifacts
- Alternative explanations

5) Unresolved questions
- What remains ambiguous?
- What discriminating experiment is needed next?

6) Cautious claims boundary
- What this artifact does NOT establish.
- No mechanism-proof language unless strict causal intervention evidence is present.

## Required sections for hidden-state / probe artifacts
- Representation object definition (final token, pooled, layer set)
- Drift metric definition and caveats
- Why metric movement does not imply semantic equivalence/non-equivalence by itself
- Probe interpretation caveat (recoverability != necessity)

## Required sections for prompt sensitivity artifacts
- Fixed-vs-perturbed components table:
  - fixed: example causal structure, label schema, model checkpoint
  - perturbed: prompt framing / terminology
- Flip-rate interpretation with uncertainty
- Why controlled perturbation is informative despite small N

## Required language constraints
- Use: suggest, indicate, consistent with, exploratory, tentative.
- Avoid: proves, demonstrates true mechanism, confirms causal reasoning internally.

## Automation policy
- `src/generate_experiment_report.py` must emit an auto-generated scientific interpretation block including:
  - emerging hypotheses,
  - non-claims,
  - confounders,
  - next mechanistic questions.
- Manual reports should extend (not replace) this block with deeper case-level reasoning.

## Review checklist before accepting a report
- [ ] Includes interpretation beyond metrics.
- [ ] Distinguishes evidence vs inference.
- [ ] States what is not shown.
- [ ] Documents confounders and unresolved questions.
- [ ] Proposes falsifiable next experiments.
