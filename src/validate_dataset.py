from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from utils import read_jsonl

REQUIRED_FIELDS = {
    'id','task_type','domain','organ','exposure','molecular_initiating_event','mediator','outcome','bias_variable',
    'study_design','vignette','question','gold_answer','gold_concepts','gold_explanation','pair_id','variant_type'
}
VALID_TASK_TYPES = {'clean_mediation','confounding','selection_bias','mechanistic_distractor'}


def validate_records(records: list[dict], dataset_name: str) -> list[str]:
    errors = []
    seen_ids = set()
    for i, rec in enumerate(records):
        missing = REQUIRED_FIELDS - set(rec.keys())
        if missing:
            errors.append(f'[{dataset_name}:{i}] Missing fields: {sorted(missing)}')
        if rec.get('gold_answer') not in {'yes', 'no'}:
            errors.append(f'[{dataset_name}:{i}] Invalid gold_answer: {rec.get("gold_answer")}')
        if rec.get('task_type') not in VALID_TASK_TYPES:
            errors.append(f'[{dataset_name}:{i}] Invalid task_type: {rec.get("task_type")}')
        gc = rec.get('gold_concepts')
        if not isinstance(gc, list) or len(gc) == 0:
            errors.append(f'[{dataset_name}:{i}] gold_concepts must be non-empty list')
        if not rec.get('pair_id'):
            errors.append(f'[{dataset_name}:{i}] pair_id missing/empty')
        if not rec.get('variant_type'):
            errors.append(f'[{dataset_name}:{i}] variant_type missing/empty')
        rid = rec.get('id')
        if rid in seen_ids:
            errors.append(f'[{dataset_name}:{i}] Duplicate id: {rid}')
        seen_ids.add(rid)
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description='Validate synthetic dataset files.')
    parser.add_argument('--datasets', nargs='*', default=[
        'data/generated/toxicity_vignettes.jsonl',
        'data/generated/ablated_vignettes.jsonl',
        'data/generated/renamed_vignettes.jsonl',
    ])
    args = parser.parse_args()

    any_errors = []
    for ds in args.datasets:
        path = Path(ds)
        records = read_jsonl(path)
        errors = validate_records(records, path.name)
        task_counts = Counter(r['task_type'] for r in records)
        variant_counts = Counter(r['variant_type'] for r in records)
        print(f'\nDataset: {path} | n={len(records)}')
        print('task_type distribution:', dict(task_counts))
        print('variant_type distribution:', dict(variant_counts))
        any_errors.extend(errors)

    if any_errors:
        print('\nValidation FAILED with issues:')
        for e in any_errors:
            print('-', e)
        raise SystemExit(1)

    print('\nValidation PASSED: all dataset checks succeeded.')


if __name__ == '__main__':
    main()
