from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from parse_outputs import parse_yes_no, concept_mentions
from utils import read_jsonl, ensure_dir


def main() -> None:
    parser = argparse.ArgumentParser(description='Score generation outputs.')
    parser.add_argument('--generations', type=str, default=None, help='Path to generations jsonl. If omitted, uses latest file in results/generations.')
    parser.add_argument('--output_dir', type=str, default='results/scores')
    args = parser.parse_args()

    gen_path = Path(args.generations) if args.generations else sorted(Path('results/generations').glob('generations_*.jsonl'))[-1]
    rows = read_jsonl(gen_path)

    scored = []
    for r in rows:
        parsed = parse_yes_no(r['model_output'])
        mentions = concept_mentions(r['model_output'])
        gold = set(r['gold_concepts'])
        recall = (len(gold.intersection(set(mentions))) / len(gold)) if gold else 0.0
        scored.append({
            'example_id': r['example_id'], 'pair_id': r['pair_id'], 'task_type': r['task_type'], 'variant_type': r['variant_type'],
            'prompt_type': r['prompt_type'], 'gold_answer': r['gold_answer'], 'parsed_answer': parsed,
            'correct': int(parsed == r['gold_answer']), 'mentioned_concepts': ';'.join(mentions), 'gold_concepts': ';'.join(r['gold_concepts']),
            'concept_recall_rough': recall, 'model_output': r['model_output']
        })

    df = pd.DataFrame(scored)
    summary = (
        df.groupby(['task_type', 'prompt_type'], as_index=False)
        .agg(n=('example_id', 'count'), accuracy=('correct', 'mean'), unclear_rate=('parsed_answer', lambda x: (x == 'unclear').mean()), concept_recall_rough=('concept_recall_rough', 'mean'))
    )

    out_dir = Path(args.output_dir)
    ensure_dir(out_dir)
    df.to_csv(out_dir / 'scored_generations.csv', index=False)
    summary.to_csv(out_dir / 'summary_by_task_and_prompt.csv', index=False)
    print(f'Saved scored outputs to {out_dir}')


if __name__ == '__main__':
    main()
