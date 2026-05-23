from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import torch
import yaml
from tqdm import tqdm

from load_model import load_model_and_tokenizer
from prompts import build_prompt
from utils import ensure_dir, load_config, read_jsonl, write_jsonl


def generate_response(
    tokenizer,
    model,
    user_prompt: str,
    max_new_tokens: int = 256,
    do_sample: bool = False,
) -> str:
    """Generate a response from a chat-style user prompt."""
    messages = [{"role": "user", "content": user_prompt}]

    prompt_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    inputs = tokenizer(
        prompt_text,
        return_tensors="pt",
    ).to(model.device)

    generation_kwargs = {
        "max_new_tokens": max_new_tokens,
        "do_sample": do_sample,
        "pad_token_id": tokenizer.eos_token_id,
    }

    if do_sample:
        generation_kwargs.update({"temperature": 0.7, "top_p": 0.9})

    with torch.no_grad():
        output_ids = model.generate(**inputs, **generation_kwargs)

    prompt_length = inputs["input_ids"].shape[-1]
    generated_ids = output_ids[0, prompt_length:]
    text = tokenizer.decode(generated_ids, skip_special_tokens=True)
    return text.strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run local generation over all examples and prompt variants."
    )
    parser.add_argument("--config", type=str, default="config.yaml")
    parser.add_argument(
        "--run_name",
        type=str,
        default="",
        help="Optional run label for file naming and traceability.",
    )
    args = parser.parse_args()

    cfg = load_config(Path(args.config))
    tokenizer, model = load_model_and_tokenizer(cfg["model_name"])

    all_examples = []
    for ds in cfg["datasets"]:
        all_examples.extend(read_jsonl(Path(ds)))

    max_new_tokens = int(cfg.get("max_new_tokens", 256))
    do_sample = bool(cfg.get("do_sample", False))

    records = []
    for ex in tqdm(all_examples, desc="Generating"):
        for prompt_type in cfg["prompt_types"]:
            prompt = build_prompt(ex, prompt_type)
            try:
                text = generate_response(
                    tokenizer=tokenizer,
                    model=model,
                    user_prompt=prompt,
                    max_new_tokens=max_new_tokens,
                    do_sample=do_sample,
                )
            except RuntimeError as e:
                if "out of memory" in str(e).lower() and torch.cuda.is_available():
                    torch.cuda.empty_cache()
                raise

            records.append(
                {
                    "model": cfg["model_name"],
                    "example_id": ex["id"],
                    "pair_id": ex["pair_id"],
                    "task_type": ex["task_type"],
                    "variant_type": ex["variant_type"],
                    "prompt_type": prompt_type,
                    "gold_answer": ex["gold_answer"],
                    "gold_concepts": ex["gold_concepts"],
                    "prompt": prompt,
                    "model_output": text,
                }
            )

    output_root = Path(cfg.get("output_dir", "results"))
    out_dir = output_root / "generations"
    metadata_dir = output_root / "metadata"
    ensure_dir(out_dir)
    ensure_dir(metadata_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = args.run_name.strip().replace(" ", "_")
    run_prefix = f"{timestamp}_{run_name}" if run_name else timestamp

    out_path = out_dir / f"generations_{run_prefix}.jsonl"
    write_jsonl(out_path, records)

    config_snapshot_path = metadata_dir / f"config_{run_prefix}.yaml"
    with config_snapshot_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)

    run_manifest = {
        "run_prefix": run_prefix,
        "timestamp": timestamp,
        "run_name": run_name or None,
        "command": "python src/run_generation.py",
        "config_source_path": str(Path(args.config)),
        "config_snapshot_path": str(config_snapshot_path),
        "generations_path": str(out_path),
        "model_name": cfg.get("model_name"),
        "max_new_tokens": cfg.get("max_new_tokens"),
        "do_sample": cfg.get("do_sample"),
        "datasets": cfg.get("datasets"),
        "prompt_types": cfg.get("prompt_types"),
        "num_examples": len(all_examples),
        "num_records": len(records),
    }
    manifest_path = metadata_dir / f"run_manifest_{run_prefix}.json"
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(run_manifest, f, indent=2)

    print(f"Saved {len(records)} generations to {out_path}")
    print(f"Saved config snapshot to {config_snapshot_path}")
    print(f"Saved run manifest to {manifest_path}")


if __name__ == "__main__":
    main()
