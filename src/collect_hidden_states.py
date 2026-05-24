from __future__ import annotations

import argparse
from pathlib import Path

import torch
from tqdm import tqdm

from load_model import load_model_and_tokenizer
from prompts import build_prompt
from utils import ensure_dir, load_config, read_jsonl


def resolve_prompt_types(cfg: dict, cli_prompt_type: str | None) -> list[str]:
    """Resolve prompt types for hidden-state collection.

    Priority:
    1) --prompt_type from CLI (single prompt)
    2) hidden_states.prompt_types in config
    3) hidden_states.prompt_type in config (legacy single value)
    4) fallback to mechanistic
    """
    if cli_prompt_type:
        return [cli_prompt_type]

    hs_cfg = cfg.get("hidden_states", {})
    if "prompt_types" in hs_cfg and hs_cfg["prompt_types"]:
        return list(hs_cfg["prompt_types"])
    if "prompt_type" in hs_cfg and hs_cfg["prompt_type"]:
        return [hs_cfg["prompt_type"]]
    return ["mechanistic"]


def collect_for_prompt(tokenizer, model, example: dict, prompt_type: str, save_mean_pool: bool) -> dict:
    """Collect per-layer activations for one example/prompt pair without text generation."""
    prompt = build_prompt(example, prompt_type)
    messages = [{"role": "user", "content": prompt}]
    input_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    ).to(model.device)

    with torch.no_grad():
        out = model(input_ids, output_hidden_states=True)

    hidden_states = out.hidden_states
    final_token = [layer_h[0, -1, :].detach().cpu() for layer_h in hidden_states]

    record = {
        "example_id": example["id"],
        "pair_id": example["pair_id"],
        "task_type": example["task_type"],
        "variant_type": example["variant_type"],
        "gold_answer": example["gold_answer"],
        "gold_concepts": example["gold_concepts"],
        "prompt_type": prompt_type,
        "final_token_by_layer": final_token,
    }

    if save_mean_pool:
        record["mean_pool_by_layer"] = [layer_h[0].mean(dim=0).detach().cpu() for layer_h in hidden_states]

    return record


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect hidden-state representations (forward pass only).")
    parser.add_argument("--config", type=str, default="config.yaml")
    parser.add_argument("--prompt_type", type=str, default=None)
    parser.add_argument("--max_examples", type=int, default=None)
    parser.add_argument("--output_path", type=str, default=None)
    args = parser.parse_args()

    cfg = load_config(Path(args.config))
    prompt_types = resolve_prompt_types(cfg, args.prompt_type)

    hs_cfg = cfg.get("hidden_states", {})
    save_mean_pool = bool(hs_cfg.get("save_mean_pool", True))
    cfg_max_examples = hs_cfg.get("max_examples", None)
    max_examples = args.max_examples if args.max_examples is not None else cfg_max_examples

    tokenizer, model = load_model_and_tokenizer(cfg["model_name"])

    examples = []
    for ds in cfg["datasets"]:
        examples.extend(read_jsonl(Path(ds)))

    if max_examples is not None:
        examples = examples[: int(max_examples)]

    records = []
    total = len(examples) * len(prompt_types)
    progress = tqdm(total=total, desc="Collecting activations")

    for ex in examples:
        for prompt_type in prompt_types:
            rec = collect_for_prompt(tokenizer, model, ex, prompt_type, save_mean_pool)
            records.append(rec)
            progress.update(1)

    progress.close()

    out_dir = Path(cfg.get("output_dir", "results")) / "activations"
    ensure_dir(out_dir)
    out_path = Path(args.output_path) if args.output_path else out_dir / "qwen2p5_hidden_states.pt"

    payload = {
        "model_name": cfg["model_name"],
        "prompt_types": prompt_types,
        "save_mean_pool": save_mean_pool,
        "num_examples": len(examples),
        "num_records": len(records),
        "records": records,
    }
    torch.save(payload, out_path)

    print(f"Saved hidden states to {out_path}")
    print(f"Examples: {len(examples)} | prompt_types: {prompt_types} | records: {len(records)}")


if __name__ == "__main__":
    main()
