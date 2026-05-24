from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split


def label_for(concepts: list[str], target: str) -> int:
    return int(target in set(concepts))


def main() -> None:
    parser = argparse.ArgumentParser(description='Train layerwise linear probes on hidden states.')
    parser.add_argument('--activations', type=str, default='results/activations/qwen2p5_hidden_states.pt')
    parser.add_argument('--output_csv', type=str, default='results/scores/probe_by_layer.csv')
    args = parser.parse_args()

    payload = torch.load(args.activations, map_location='cpu')
    records = payload['records']
    n_layers = len(records[0]['final_token_by_layer'])

    concepts = ['confounding', 'mediation', 'selection_bias']
    rows = []

    for concept in concepts:
        y = np.array([label_for(r['gold_concepts'], concept) for r in records])
        if y.min() == y.max():
            print(f'Skipping {concept}: single-class labels in this dataset.')
            continue
        for layer in range(n_layers):
            X = np.stack([r['final_token_by_layer'][layer].numpy() for r in records])
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
            clf = LogisticRegression(max_iter=1000)
            clf.fit(X_train, y_train)
            pred = clf.predict(X_test)
            rows.append({
                'concept': concept,
                'layer': layer,
                'n_train': len(y_train),
                'n_test': len(y_test),
                'accuracy': accuracy_score(y_test, pred),
                'f1': f1_score(y_test, pred),
            })

    out = pd.DataFrame(rows)
    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output_csv, index=False)
    print('Saved probe results to', args.output_csv)
    print('Interpretation note: probe performance indicates linear recoverability, not proof of causal use by the model.')


if __name__ == '__main__':
    main()
