from __future__ import annotations

import argparse
import random
from pathlib import Path

from utils import write_jsonl, ensure_dir

TASK_TYPES = ['clean_mediation', 'confounding', 'selection_bias', 'mechanistic_distractor']
ORGANS = ['liver', 'kidney', 'heart', 'lung', 'immune system', 'nervous system']
EXPOSURES = ['Drug A', 'Drug B', 'Drug C', 'Drug D']
MIES = ['enzyme E activation', 'receptor R inhibition', 'metabolite M accumulation', 'mitochondrial stress signal']
MEDIATORS = ['oxidative stress', 'inflammatory cytokine C response', 'cellular calcium imbalance', 'membrane transport disruption']
OUTCOMES = ['tissue injury signal', 'toxicity marker elevation', 'adverse functional decline', 'cell death index increase']
BIAS_VARIABLES = ['baseline frailty', 'co-medication pattern', 'disease severity', 'care access intensity']
DESIGNS = ['observational cohort', 'case-control registry', 'single-center observational study']


def make_example(idx: int, task_type: str, rng: random.Random) -> dict:
    pair_id = f'pair_{idx:03d}'
    organ = rng.choice(ORGANS)
    exposure = rng.choice(EXPOSURES)
    mie = rng.choice(MIES)
    mediator = rng.choice(MEDIATORS)
    outcome = rng.choice(OUTCOMES)
    bias = rng.choice(BIAS_VARIABLES)
    design = rng.choice(DESIGNS)

    if task_type == 'clean_mediation':
        gold_answer = 'yes'
        concepts = ['mediation', 'mechanism']
        vignette = (
            f'In a synthetic {design}, higher {exposure} exposure precedes {mie}, then {mediator}, '
            f'followed by {organ} {outcome}. Timing is consistent across sites with no strong alternative driver reported.'
        )
        explanation = 'The proposed causal chain is internally consistent with mediation in this synthetic scenario.'
    elif task_type == 'confounding':
        gold_answer = 'no'
        concepts = ['confounding', 'observational association']
        vignette = (
            f'In a synthetic {design}, {exposure} exposure is associated with {organ} {outcome}, but {bias} '
            f'plausibly increases both exposure likelihood and outcome risk. Mechanistic measurements are sparse.'
        )
        explanation = 'A confounder could explain the association without supporting the causal claim.'
    elif task_type == 'selection_bias':
        gold_answer = 'no'
        concepts = ['selection_bias', 'collider']
        vignette = (
            f'A synthetic toxicity analysis includes only participants who returned for intensive follow-up, where return probability '
            f'depends on both {exposure} exposure and early {organ} symptoms related to {outcome}. '
            f'This conditioning may induce a collider-like distortion.'
        )
        explanation = 'Selection can induce biased associations that weaken causal support.'
    else:
        gold_answer = 'no'
        concepts = ['mechanism', 'observational association']
        vignette = (
            f'A synthetic {design} reports a detailed story about {mie} and {mediator}, but exposure-to-outcome ordering is unclear and '
            f'alternative pathways are not ruled out for {organ} {outcome}. Biological language is rich but evidential support is limited.'
        )
        explanation = 'Mechanistic detail alone does not establish the causal claim in this synthetic vignette.'

    return {
        'id': f'{task_type}_{idx:03d}_orig',
        'task_type': task_type,
        'domain': 'drug_toxicity',
        'organ': organ,
        'exposure': exposure,
        'molecular_initiating_event': mie,
        'mediator': mediator,
        'outcome': outcome,
        'bias_variable': bias,
        'study_design': design,
        'vignette': vignette,
        'question': 'Is the claim that the exposure causes the adverse outcome through the proposed mechanism supported?',
        'gold_answer': gold_answer,
        'gold_concepts': concepts,
        'gold_explanation': explanation,
        'pair_id': pair_id,
        'variant_type': 'original',
    }


def make_ablations(example: dict) -> list[dict]:
    out = []
    base = dict(example)

    c = dict(base)
    c['id'] = base['id'].replace('_orig', '_abl_conf_removed')
    c['variant_type'] = 'confounder_removed'
    c['vignette'] = base['vignette'].replace(base['bias_variable'], 'an unmeasured background factor') + ' Confounder evidence is intentionally removed.'
    c['gold_answer'] = 'yes' if base['task_type'] == 'confounding' else base['gold_answer']
    c['gold_concepts'] = [g for g in base['gold_concepts'] if g != 'confounding'] or ['mediation']
    out.append(c)

    m = dict(base)
    m['id'] = base['id'].replace('_orig', '_abl_med_removed')
    m['variant_type'] = 'mediator_removed'
    m['vignette'] = base['vignette'].replace(base['mediator'], 'an unspecified intermediate') + ' Mediator measurements are omitted.'
    m['gold_answer'] = 'no'
    if 'mediation' in m['gold_concepts']:
        m['gold_concepts'] = [g for g in m['gold_concepts'] if g != 'mediation'] + ['observational association']
    out.append(m)

    r = dict(base)
    r['id'] = base['id'].replace('_orig', '_abl_randomized')
    r['variant_type'] = 'randomized_design'
    r['study_design'] = 'randomized synthetic trial'
    r['vignette'] = base['vignette'] + ' Assignment is randomized in this variant.'
    r['gold_concepts'] = sorted(set(r['gold_concepts'] + ['randomization']))
    if base['task_type'] in {'confounding', 'selection_bias'}:
        r['gold_answer'] = 'yes'
    out.append(r)

    s = dict(base)
    s['id'] = base['id'].replace('_orig', '_abl_selection_added')
    s['variant_type'] = 'selection_bias_added'
    s['vignette'] = base['vignette'] + ' Analysis includes only participants selected by both exposure level and early symptoms.'
    s['gold_answer'] = 'no'
    s['gold_concepts'] = sorted(set(s['gold_concepts'] + ['selection_bias']))
    out.append(s)

    return out


def make_renamed(example: dict) -> dict:
    replacements = {
        'Drug A': 'Treatment A', 'Drug B': 'Treatment B', 'Drug C': 'Treatment C', 'Drug D': 'Treatment D',
        'enzyme E': 'Variable B', 'receptor R': 'Variable C', 'metabolite M': 'Variable B',
        'toxicity': 'Outcome D', 'injury': 'Outcome D', 'adverse': 'Outcome D'
    }
    text = example['vignette']
    for k, v in replacements.items():
        text = text.replace(k, v)
    r = dict(example)
    r['id'] = example['id'].replace('_orig', '_renamed')
    r['variant_type'] = 'renamed_terms'
    r['vignette'] = text
    r['question'] = example['question'].replace('exposure', 'treatment').replace('adverse outcome', 'Outcome D')
    return r


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate synthetic toxicity causal reasoning datasets.')
    parser.add_argument('--n', type=int, default=48, help='Number of original examples (>=40 recommended).')
    parser.add_argument('--seed', type=int, default=7)
    parser.add_argument('--out_dir', type=str, default='data/generated')
    args = parser.parse_args()

    rng = random.Random(args.seed)
    out_dir = Path(args.out_dir)
    ensure_dir(out_dir)

    originals = []
    for i in range(args.n):
        task_type = TASK_TYPES[i % len(TASK_TYPES)]
        originals.append(make_example(i + 1, task_type, rng))

    ablated = []
    renamed = []
    for ex in originals:
        ablated.extend(make_ablations(ex))
        renamed.append(make_renamed(ex))

    write_jsonl(out_dir / 'toxicity_vignettes.jsonl', originals)
    write_jsonl(out_dir / 'ablated_vignettes.jsonl', ablated)
    write_jsonl(out_dir / 'renamed_vignettes.jsonl', renamed)

    print(f'Wrote originals: {len(originals)}')
    print(f'Wrote ablations: {len(ablated)}')
    print(f'Wrote renamed: {len(renamed)}')


if __name__ == '__main__':
    main()
