from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import torch


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def build_index(records: list[dict]) -> dict[tuple[str, str], dict]:
    return {(r["example_id"], r.get("prompt_type", "mechanistic")): r for r in records}


def layerwise_metric(vecs_a: list, vecs_b: list, metric: str) -> list[float]:
    vals: list[float] = []
    for a_t, b_t in zip(vecs_a, vecs_b):
        a = a_t.numpy()
        b = b_t.numpy()
        sim = cosine_similarity(a, b)
        vals.append(1.0 - sim if metric == "distance" else sim)
    return vals


def main() -> None:
    parser = argparse.ArgumentParser(description="Prompt-conditioned latent drift and representation stability analysis.")
    parser.add_argument("--activations", type=str, default="results/activations/qwen2p5_hidden_states.pt")
    parser.add_argument("--output_csv", type=str, default="results/scores/prompt_latent_drift.csv")
    parser.add_argument("--summary_csv", type=str, default="results/scores/prompt_latent_drift_summary.csv")
    parser.add_argument("--baseline_prompt", type=str, default="mechanistic")
    parser.add_argument("--compare_prompts", type=str, nargs="*", default=["confounding_aware", "adversarial"])
    args = parser.parse_args()

    payload = torch.load(args.activations, map_location="cpu")
    records = payload["records"]
    index = build_index(records)

    example_ids = sorted(set(r["example_id"] for r in records))
    rows = []

    for ex_id in example_ids:
        base_key = (ex_id, args.baseline_prompt)
        if base_key not in index:
            continue
        base = index[base_key]

        for compare_prompt in args.compare_prompts:
            cmp_key = (ex_id, compare_prompt)
            if cmp_key not in index:
                continue

            cmp_rec = index[cmp_key]
            final_dists = layerwise_metric(base["final_token_by_layer"], cmp_rec["final_token_by_layer"], metric="distance")

            mean_dists = None
            if "mean_pool_by_layer" in base and "mean_pool_by_layer" in cmp_rec:
                mean_dists = layerwise_metric(base["mean_pool_by_layer"], cmp_rec["mean_pool_by_layer"], metric="distance")

            for layer, dist in enumerate(final_dists):
                row = {
                    "example_id": ex_id,
                    "pair_id": base["pair_id"],
                    "task_type": base["task_type"],
                    "variant_type": base["variant_type"],
                    "baseline_prompt": args.baseline_prompt,
                    "compare_prompt": compare_prompt,
                    "layer": layer,
                    "cosine_distance_final_token": dist,
                    "cosine_distance_mean_pool": np.nan,
                }
                if mean_dists is not None:
                    row["cosine_distance_mean_pool"] = mean_dists[layer]
                rows.append(row)

    drift_df = pd.DataFrame(rows)
    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
    drift_df.to_csv(args.output_csv, index=False)

    if drift_df.empty:
        print("No comparable prompt pairs found. Check hidden-state prompt_types and analysis arguments.")
        return

    summary = (
        drift_df.groupby(["task_type", "variant_type", "baseline_prompt", "compare_prompt", "layer"], as_index=False)
        .agg(
            n_examples=("example_id", "nunique"),
            mean_cosine_distance_final_token=("cosine_distance_final_token", "mean"),
            mean_cosine_distance_mean_pool=("cosine_distance_mean_pool", "mean"),
        )
    )
    summary.to_csv(args.summary_csv, index=False)

    print(f"Saved prompt latent drift rows: {len(drift_df)} -> {args.output_csv}")
    print(f"Saved prompt latent drift summary: {args.summary_csv}")


if __name__ == "__main__":
    main()
