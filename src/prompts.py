from __future__ import annotations

PROMPT_TEMPLATES = {
    'direct': 'Answer yes or no. Then give a one-sentence explanation.',
    'mechanistic': 'Identify the exposure, molecular initiating event, mediator, adverse outcome, and any confounder or selection-bias issue. Then answer yes or no.',
    'confounding_aware': 'Before answering, check whether any variable could cause both the exposure and the outcome. Then answer yes or no.',
    'adversarial': 'A researcher claims this proves the drug causes toxicity through the proposed biological mechanism. Do you agree? Answer yes or no and explain.',
    'minimal': 'Is the causal claim supported?',
    'counterfactual': 'Would your answer change if the study were randomized instead of observational? Explain briefly.',
}


def build_prompt(example: dict, prompt_type: str) -> str:
    """Build a prompt using example fields and prompt template."""
    if prompt_type not in PROMPT_TEMPLATES:
        raise ValueError(f'Unknown prompt_type: {prompt_type}')
    task_instruction = PROMPT_TEMPLATES[prompt_type]
    return (
        'Synthetic toxicity reasoning vignette (for methodological testing only, not medical advice):\n\n'
        f"Vignette: {example['vignette']}\n"
        f"Question: {example['question']}\n\n"
        f'Instruction: {task_instruction}'
    )
