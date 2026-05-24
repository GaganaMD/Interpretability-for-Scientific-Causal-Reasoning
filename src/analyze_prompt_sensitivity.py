from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description='Analyze prompt sensitivity from scored generations CSV.')
    parser.add_argument('--scored_csv', type=str, default='results/scores/scored_generations.csv')
    parser.add_argument('--output_csv', type=str, default='results/scores/prompt_stability.csv')
    args = parser.parse_args()

    df = pd.read_csv(args.scored_csv)

    rows = []
    for ex_id, g in df.groupby('example_id'):
        answers = list(g['parsed_answer'])
        unique_answers = sorted(set(answers))
        majority = pd.Series(answers).mode().iloc[0]
        stability = max(answers.count(a) for a in unique_answers) / len(answers)
        rows.append({
            'example_id': ex_id,
            'pair_id': g['pair_id'].iloc[0],
            'task_type': g['task_type'].iloc[0],
            'variant_type': g['variant_type'].iloc[0],
            'num_prompt_variants': len(answers),
            'parsed_answer_set': '|'.join(unique_answers),
            'majority_answer': majority,
            'stability_score': stability,
            'any_prompt_flip': int(len(unique_answers) > 1),
        })

    out = pd.DataFrame(rows)
    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output_csv, index=False)
    print(f'Saved prompt stability analysis: {args.output_csv}')


if __name__ == '__main__':
    main()
