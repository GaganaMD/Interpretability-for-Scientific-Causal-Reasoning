# Research Evolution Notes: Prompt-Conditioned Causal Reasoning Instability in Qwen2.5

## 0) Purpose of this document
This document is a research artifact, not a user-facing summary. Its role is to preserve the scientific trajectory of the project: what we tested, what signals emerged, why they are mechanistically interesting, what remains unresolved, and how this should shape next-phase experiments.

The project has shifted from a generic synthetic QA benchmark mindset toward a controlled interpretability setup centered on stability, invariance, and latent abstraction behavior.

## 1) Conceptual evolution of the project
Initial framing:
- Build synthetic causal toxicity tasks and test whether a local open model can answer yes/no causal questions.

Current framing:
- Hold causal structure fixed and perturb prompt framing/terminology.
- Measure behavioral instability under controlled perturbations.
- Treat instability as a signal motivating latent-space analysis.
- Explicitly distinguish behavioral differences from representational differences.

Interpretability significance:
- This reframing changes the core question from capability to mechanism-adjacent stability.
- We now ask whether the model applies a stable causal abstraction, or whether decisions are largely prompt-contingent policies.

## 2) Why the 48-example / 192-record structure matters
The core analysis run has 48 unique examples but 192 records because each example is evaluated under 4 prompt framings.

48 examples x 4 prompts = 192 records.

Scientific importance:
- The underlying causal vignette can remain constant while instruction framing changes.
- This creates a matched within-example perturbation design.
- The design is stronger for interpretability than naive aggregate benchmarking because it isolates framing sensitivity without changing the target reasoning object.

This is closer to controlled intervention logic than to leaderboard-style evaluation.

## 3) Why multiple prompt framings were introduced
Prompt framings (direct, mechanistic, confounding-aware, adversarial) were introduced to test whether instruction context changes inferred reasoning policy.

Design rationale:
- direct: baseline instruction following.
- mechanistic: asks for explicit mechanism-focused reasoning.
- confounding-aware: encourages statistical caution around causal confounds.
- adversarial: encourages skeptical discrimination and error avoidance.

Interpretability relevance:
- If a stable internal causal abstraction exists and is robustly used, output decisions should be relatively invariant across framing shifts.
- Large framing-dependent flips suggest context-sensitive policy routing, weak abstraction anchoring, or both.

## 4) Why renamed terminology variants matter
Renaming keeps intended causal structure while perturbing lexical anchors.

Scientific value:
- Tests semantic anchoring vs abstraction invariance.
- If abstraction is robust, variable renaming should not strongly alter final judgments.
- If renaming changes behavior materially, the model may rely on surface correlations tied to familiar biomedical tokens.

This is a cleaner mechanistic stressor than many benchmark perturbations because causal skeleton is intended to remain comparable while lexical realization shifts.

## 5) Why adversarial prompts are scientifically interesting
Adversarial framing often outperformed other framings in current results.

Possible meaning:
- The model may perform better when prompted into discriminative skepticism.
- This can indicate better heuristic filtering, not necessarily better causal understanding.

Interpretability concern:
- Improved task accuracy under adversarial framing could still be non-mechanistic (shortcut-heavy).
- A key open question is whether higher performance here corresponds to more stable latent abstractions or merely stronger local decision heuristics.

## 6) Why weak mechanistic-prompt performance is notable
Mechanistic prompting underperformed in current behavior summaries.

Potential interpretations:
1) Mechanistic-language overload in a small checkpoint may destabilize decision quality.
2) The model may produce plausible mechanistic rhetoric without stable mechanistic computation.
3) Mechanistic prompt tokens may activate incompatible priors for this task template.

Research meaning:
- This result cautions against assuming that “more mechanistic instruction” improves mechanistic reasoning.
- It reinforces the faithfulness problem: explanation style and decision quality can decouple.

## 7) Why prompt flip rate is interpretability-relevant
Observed flip behavior is high in the current renamed-variant run (mean stability ~0.745 with flip rate 1.0 across examples in prompt_stability.csv).

Why this matters:
- A flip means same example, different prompt framing, different final yes/no decision.
- High flip prevalence implies unstable decision boundaries in prompt-conditioned context.
- This is direct evidence of behavioral non-invariance under controlled framing perturbation.

Cautious interpretation:
- High flip rate alone does not prove latent mechanism switching.
- But it is a strong trigger for hidden-state and representation-drift analysis.

## 8) Current empirical signals from available artifacts
Grounded in current score files and trace report:
- Latest scored dataset: 192 records, renamed_terms variant.
- Overall accuracy ~0.505.
- Prompt-level mean accuracy: adversarial 0.75, direct ~0.521, confounding_aware 0.5, mechanistic 0.25.
- Prompt stability mean ~0.745, example-level flip rate 1.0.

Interpretation of pattern:
- Accuracy is not catastrophically low, but is strongly prompt-conditioned.
- Performance ranking across prompt types suggests prompt priors matter as much as or more than stable task abstraction.
- Instability persists even in a controlled synthetic setup.

## 9) Behavioral instability vs representation instability
Critical distinction:
- Behavioral instability: output label changes across prompts.
- Representation instability: hidden-state geometry shifts across prompts.

They are related but not equivalent.
- You can observe output flips with moderate latent drift if the decision boundary is near threshold.
- You can observe latent drift without flips if drift remains within same classification region.

Therefore, current behavioral findings motivate but do not settle representation-level conclusions.

## 10) Why hidden-state analysis is the natural next phase
Given high prompt-conditioned flipping, hidden-state analysis became necessary to answer:
- Where in depth does prompt reframing perturb representations most?
- Are drift patterns prompt-specific or task-type-specific?
- Do renamed terms induce drift profiles similar to causal-structure perturbations or distinct from them?

This motivated:
- selective hidden-state extraction,
- activation contrasts (original vs variant),
- and prompt-pair latent drift tooling.

## 11) Emerging hypotheses (explicitly tentative)
H1. Prompt-prior reliance hypothesis:
- The model may rely on framing-conditioned priors more than a stable causal abstraction.

H2. Adversarial heuristic-discrimination hypothesis:
- Adversarial prompts may improve discriminative heuristics without improving mechanism-faithful reasoning.

H3. Mechanistic destabilization hypothesis:
- Explicit mechanistic prompting may degrade weaker-model performance by increasing instruction complexity and activating less reliable reasoning policies.

H4. Terminology anchoring hypothesis:
- Renaming terms may expose shallow abstraction formation and lexical dependence.

H5. Prompt-conditioned latent drift hypothesis:
- Behavioral flips reflect, at least partially, prompt-conditioned representational drift in middle/late layers.

## 12) What current experiments do NOT show
- Probes (if/when trained) do not prove mechanism; they show decodability/recoverability.
- Hidden-state cosine similarity does not prove reasoning equivalence or causal abstraction identity.
- Behavioral instability alone does not establish causal failure; it establishes sensitivity under tested perturbations.
- Synthetic toxicity setup does not demonstrate real biomedical competence.
- No claim should be made that this uncovers “true internal mechanism” at current stage.

## 13) Limitations that directly affect interpretation
- Small sample size (48 unique examples) improves control but limits statistical confidence.
- Parsing/scoring are intentionally lightweight and may miss nuanced outputs.
- Current analyzed score artifact is dominated by renamed_terms variant.
- Hidden-state analyses are partially infrastructure-complete but not yet fully executed end-to-end in this environment due model fetch/connectivity constraints.

## 14) Why small controlled studies remain valuable
Even with modest scale, the controlled perturbation structure can reveal strong invariance failures quickly.

This differs from large noisy benchmark sweeps:
- Large sweeps provide breadth but can obscure mechanism-relevant signals.
- Controlled perturbations provide cleaner local evidence for instability hypotheses.

For early mechanistic exploration, this is often the right tradeoff.

## 15) Forward research trajectory
Priority directions:
1) Layerwise latent drift mapping
- Compare prompt pairs on same example, layer by layer.
- Identify depth regions with maximal prompt sensitivity.

2) Prompt-pair representation geometry
- Cluster by prompt type and task type.
- Test whether adversarial/mechanistic states occupy separable regions.

3) Causal-structure vs lexical perturbation decomposition
- Compare drift induced by renamed_terms vs graph edits (confounder_removed, mediator_removed, etc.).
- Ask whether lexical changes can rival true structure edits in drift magnitude.

4) Checkpoint scaling sweep
- Repeat on Qwen2.5 1.5B/3B as feasible.
- Measure whether flip rate and drift dispersion shrink with scale.

5) Probe robustness studies
- Evaluate layerwise probe stability across prompts and variants.
- Test whether probe separability survives lexical renaming.

6) Chain-of-thought faithfulness-oriented diagnostics
- If rationale prompting is added, compare rationale style shifts with latent drift and answer flips.
- Avoid equating articulate rationale with mechanistic faithfulness.

## 16) Practical interpretation discipline for this project
Every phase artifact should include:
- Experimental meaning (not just metric tables).
- Mechanistic interpretation hypotheses.
- Explicit uncertainty/limitations.
- Plausible confounders and alternative explanations.
- Next targeted questions that could falsify current interpretation.

This preserves scientific trajectory and avoids benchmark theater.

## 17) Current bottom line
The strongest current signal is not “causal reasoning solved.”
The strongest signal is prompt-conditioned instability under fixed underlying examples, including heavy answer flipping and strong prompt performance dispersion.

That instability is scientifically meaningful, interpretable, and actionable:
- meaningful because it challenges invariance expectations,
- interpretable because perturbations are controlled,
- actionable because it motivates specific latent-space experiments now implemented in the codebase.
