from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import torch


def cos_dist(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return 1.0 - float(np.dot(a, b) / denom)


def main() -> None:
    parser = argparse.ArgumentParser(description="Layerwise activation contrast analysis via cosine distance.")
    parser.add_argument("--activations", type=str, default="results/activations/qwen2p5_hidden_states.pt")
    parser.add_argument("--output_csv", type=str, default="results/scores/activation_contrasts.csv")
    parser.add_argument("--prompt_type", type=str, default="mechanistic", help="Use one prompt type to isolate variant effects.")
    args = parser.parse_args()

    payload = torch.load(args.activations, map_location="cpu")
    raw_records = payload["records"]
    records = [r for r in raw_records if r.get("prompt_type", "mechanistic") == args.prompt_type]

    if not records:
        raise ValueError(f"No records found for prompt_type={args.prompt_type}")

    by_pair = {}
    for r in records:
        by_pair.setdefault(r["pair_id"], []).append(r)

    rows = []
    for pair_id, group in by_pair.items():
        original = [g for g in group if g["variant_type"] == "original"]
        if not original:
            continue
        o = original[0]

        for g in group:
            if g["variant_type"] == "original":
                continue

            n_layers = len(o["final_token_by_layer"])
            for layer in range(n_layers):
                row = {
                    "pair_id": pair_id,
                    "task_type": o["task_type"],
                    "prompt_type": args.prompt_type,
                    "contrast_type": f"original_vs_{g['variant_type']}",
                    "layer": layer,
                    "cosine_distance_final_token": cos_dist(
                        o["final_token_by_layer"][layer].numpy(),
                        g["final_token_by_layer"][layer].numpy(),
                    ),
                    "cosine_distance_mean_pool": np.nan,
                }

                if "mean_pool_by_layer" in o and "mean_pool_by_layer" in g:
                    row["cosine_distance_mean_pool"] = cos_dist(
                        o["mean_pool_by_layer"][layer].numpy(),
                        g["mean_pool_by_layer"][layer].numpy(),
                    )

                rows.append(row)

    out = pd.DataFrame(rows)
    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output_csv, index=False)
    print(f"Saved activation contrast analysis to {args.output_csv} with {len(out)} rows")


if __name__ == "__main__":
    main()
