# Interpretability Experiment Report — Detailed Takeaways and Emerging Research Directions

## High-Level Summary

The current experiments already demonstrate several meaningful interpretability and causal reasoning phenomena despite:

* using a very small open model (`Qwen2.5-0.5B-Instruct`),
* operating on synthetic datasets,
* and using relatively lightweight evaluation infrastructure.

The most important emerging pattern is not simply model accuracy.

The more important observation is that:

* reasoning behavior appears highly prompt-dependent,
* causal judgments are unstable under reframing,
* and representation/abstraction robustness may be weak under terminology and contextual perturbation.

The project is increasingly becoming less about:

> “Can the model answer toxicity questions?”

and more about:

> “How stable are latent causal reasoning behaviors under prompt, terminology, and framing perturbations?”

This is much more aligned with modern mechanistic interpretability and reasoning-faithfulness research.

---

# Infrastructure and Engineering Takeaways

## 1. The experimental infrastructure is functioning successfully

The project already supports:

* synthetic dataset generation,
* prompt templating,
* multi-run evaluation,
* scoring pipelines,
* prompt perturbation analysis,
* result tracking,
* and reproducible generation artifacts.

This means the project has already moved beyond:

* toy scripts,
* single-prompt experiments,
* or ad hoc evaluations.

The repository is becoming a small interpretability benchmarking framework.

---

## 2. Multi-prompt evaluation was a strong design decision

The use of multiple prompt styles:

* direct
* mechanistic
* confounding-aware
* adversarial

was extremely important.

This transformed the experiment from:

> “single-prompt evaluation”

into:

> “reasoning stability analysis under framing perturbation.”

This is a much more interpretability-relevant setup.

---

## 3. The experiment structure is scientifically cleaner than typical benchmark evaluations

The same underlying causal examples were reused across multiple prompt framings.

This means:

* underlying causal structure remained fixed,
* labels remained fixed,
* task distribution remained fixed,
* while prompt framing changed.

This isolates:

* prompt dependence,
* framing sensitivity,
* and representational instability

more cleanly than ordinary benchmark evaluation.

---

# Dataset and Experimental Structure Takeaways

## 4. The 48-example structure is more important than it initially appears

There were:

* 48 unique underlying examples,
* but 192 total records.

This occurred because:

* each example was evaluated under 4 prompt framings.

Therefore:

48 examples × 4 prompt types = 192 records

This means the experiment is fundamentally testing:

> stability under reframing.

Not merely:

> raw accuracy.

This is an important distinction.

---

## 5. Small controlled datasets may actually be advantageous here

Despite only having:

* 48 core examples,
* relatively small synthetic datasets,
* and lightweight infrastructure,

the experiments already exposed:

* major prompt sensitivity,
* reasoning instability,
* and abstraction fragility.

This suggests the effects are:

* strong,
* detectable,
* and not dependent on massive scale.

This is consistent with many mechanistic interpretability workflows where:

* carefully controlled small experiments
  often provide more insight than large noisy benchmark sweeps.

---

## 6. The task taxonomy is well aligned with causal reasoning research

The project already includes:

* clean mediation
* confounding
* mechanistic distractors
* selection bias

This is significant because:

* confounding
* mediation
* and selection bias

are genuine causal reasoning stress tests.

This gives the benchmark stronger interpretability and reasoning relevance than ordinary QA tasks.

---

# Prompt Sensitivity and Reasoning Stability Takeaways

## 7. Prompt framing dramatically changes behavior

One of the strongest findings is that:

* model performance changes heavily depending on prompt framing.

Observed accuracies:

* adversarial: ~0.83
* direct: ~0.50
* confounding-aware: ~0.50
* mechanistic: ~0.29

This is extremely important.

The same underlying examples produced substantially different outputs under different reasoning framings.

This strongly suggests:

* reasoning is context-dependent,
* prompt framing changes internal behavior,
* and latent representations may not be stable.

---

## 8. Mechanistic prompts unexpectedly performed the worst

This is one of the most interesting findings so far.

Intuitively, one might expect:

* explicit mechanistic prompting
  to improve causal reasoning quality.

Instead:

* mechanistic prompts produced the lowest accuracy.

Possible interpretations include:

### A. Weak mechanistic abstractions

The model may not possess robust causal/mechanistic abstractions internally.

### B. Reasoning overload

Explicit mechanistic prompting may overload a small model and destabilize reasoning.

### C. Plausible-but-unfaithful reasoning

The model may generate more scientific-sounding reasoning while actually becoming less accurate.

This directly connects to:

* faithfulness research,
* chain-of-thought skepticism,
* and interpretability concerns around plausible explanations.

---

## 9. Adversarial prompts performing best is highly suspicious and interesting

Adversarial prompting achieved the highest performance.

Possible interpretations:

### A. The prompt accidentally introduced clearer decision heuristics

### B. The framing constrained generation more effectively

### C. The model responds better to contrastive/discriminative reasoning than mechanistic reasoning

### D. The model may be exploiting shortcuts rather than stable causal reasoning

This may suggest:

* adversarial framing induces heuristic discrimination,
* while mechanistic prompting destabilizes representations.

This is highly relevant to:

* reasoning faithfulness,
* shortcut learning,
* and interpretability evaluation.

---

## 10. Prompt flip rates are extremely high

Observed flip rates:

* 0.875
* later 1.000

This means:

* changing prompt framing frequently changed the model’s answer for the same example.

This is probably one of the strongest results in the entire report.

Interpretation:

* reasoning outputs are highly prompt contingent,
* causal judgments are unstable,
* representations may not encode robust causal structure.

This is strongly aligned with:

* representation invariance concerns,
* faithfulness evaluation,
* and prompt-conditioned reasoning dynamics.

---

## 11. Prompt stability degradation under renamed variables is especially important

The renamed-vignette experiments introduced terminology perturbations.

The fact that:

* stability scores dropped,
* and flip rates increased,

suggests:

* the model relies significantly on surface forms and terminology anchors.

This is important because:
a genuinely robust causal abstraction should ideally survive:

* variable renaming,
* paraphrase,
* or terminology substitutions.

Instead:

* reasoning behavior shifted noticeably.

This suggests:

* abstractions may be shallow,
* semantic anchoring matters heavily,
* and latent causal representations may not be invariant.

---

# Representation and Conceptual Takeaways

## 12. The project is implicitly testing representation invariance

The renamed-vignette experiments are not merely dataset perturbations.

They are effectively probing:

> whether latent causal reasoning survives semantic renaming.

This is very close to:

* representation robustness,
* abstraction stability,
* and manifold invariance style questions.

The experiments are beginning to probe:

* whether causal concepts remain stable across contextual perturbation.

---

## 13. Concept recall degradation is meaningful

Concept recall roughly decreased across runs:

* ~0.51
* ~0.33
* ~0.29

This may indicate:

* causal concepts become less consistently activated,
* reasoning structure degrades under perturbation,
* and abstraction salience weakens under reframing.

This supports the idea that:

* causal reasoning may not be deeply stable in the model.

---

## 14. The experiments suggest reasoning may be prompt-conditioned rather than abstraction-driven

One emerging interpretation is:

The model may not possess:

* stable causal representations,

but instead dynamically shifts behavior depending on:

* framing,
* wording,
* contextual cues,
* and prompt priors.

The prompt styles implicitly encode different “reasoning modes”:

* direct → ordinary QA
* mechanistic → explicit scientific reasoning
* confounding-aware → statistical caution
* adversarial → discriminative skepticism

The model appears highly sensitive to these contextual reasoning priors.

---

# Mechanistic Interpretability Relevance

## 15. The project is becoming more mech-interp relevant than originally expected

Initially the project may have seemed like:

* synthetic toxicity QA.

But it is increasingly becoming a study of:

* representation stability,
* prompt-conditioned reasoning,
* abstraction fragility,
* and causal invariance.

This is much closer to:

* mechanistic interpretability,
* representation analysis,
* and reasoning-faithfulness research.

---

## 16. The project naturally leads toward hidden-state analysis

The current behavioral instability strongly motivates:

* activation analysis,
* hidden-state extraction,
* and representation comparison.

The next logical question becomes:

> “Do prompt perturbations alter latent causal representations?”

This creates opportunities for:

* cosine similarity analysis,
* layerwise drift analysis,
* prompt trajectory comparison,
* and hidden-state stability studies.

---

## 17. The project may evolve toward representation geometry questions

Even though representation geometry was not initially the core focus, the current findings naturally connect to questions like:

* Do causal prompts cluster together?
* Does adversarial prompting alter latent trajectories?
* Are mechanistic prompts geometrically unstable?
* Does terminology renaming induce latent drift?
* Do causal abstractions occupy stable regions in representation space?

This opens possible future directions involving:

* hidden-state similarity,
* clustering,
* PCA/UMAP exploration,
* and representation trajectory analysis.

---

# Scientific and Research Framing Takeaways

## 18. The strongest findings are about instability, not capability

The project’s value is increasingly not:

> “the model solved causal reasoning.”

The stronger contribution is:

> “the model’s causal reasoning behavior appears unstable under prompt and terminology perturbation.”

This is a much more interesting interpretability result.

---

## 19. The project aligns strongly with modern concerns about chain-of-thought faithfulness

One implicit emerging theme is:

* more explicit reasoning prompts did not improve reasoning quality.

This challenges simplistic assumptions like:

> “more reasoning text implies better reasoning.”

The experiments may support the broader idea that:

* plausible explanations
  are not necessarily faithful explanations.

---

## 20. The experiments already support cautious but meaningful research claims

A careful claim supported by the current results might be:

> “Model outputs exhibited substantial prompt-contingent instability despite fixed underlying causal structure, suggesting that causal reasoning behavior may depend heavily on contextual framing rather than stable abstraction.”

This is already a legitimate interpretability-style observation.

---

# Immediate Next-Step Recommendations

## 21. Hidden-state analysis is now the highest-value next step

The strongest next direction is probably:

* extracting hidden states,
* comparing representations across prompts,
* and measuring latent drift.

Suggested analyses:

* cosine similarity
* layerwise similarity
* representation stability across paraphrases
* same-example hidden-state comparisons

---

## 22. Scaling should be secondary to analysis quality

The current experiments already reveal meaningful effects.

The priority should probably be:

* deeper analysis,
  not:
* larger models,
* larger datasets,
* or benchmark scaling.

The current setup is already scientifically productive.

---

## 23. Moving to Qwen2.5-1.5B is likely the ideal next compute step

The current 0.5B experiments already show:

* meaningful instability,
* prompt dependence,
* and causal fragility.

Moving to:
`Qwen2.5-1.5B-Instruct`

may help determine:

* whether these effects persist at slightly stronger capability levels,
  while remaining computationally manageable on local hardware.

---

# Final Reflection

The most important realization from the current experiments is that the project has evolved beyond a simple synthetic benchmark.

It is becoming an investigation into:

* prompt-conditioned reasoning behavior,
* causal abstraction stability,
* representation robustness,
* and the fragility of mechanistic reasoning under contextual perturbation.

This is much more aligned with modern mechanistic interpretability and scientific reasoning evaluation research than a simple QA benchmark pipeline.
