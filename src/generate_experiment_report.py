from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from statistics import mean

import pandas as pd
import yaml

from parse_outputs import concept_mentions, parse_yes_no


def read_jsonl(path: Path):
    out = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def score_records(records: list[dict]) -> pd.DataFrame:
    rows = []
    for r in records:
        parsed = parse_yes_no(r.get("model_output", ""))
        gold = r.get("gold_answer")
        mentions = concept_mentions(r.get("model_output", ""))
        gold_concepts = r.get("gold_concepts", []) or []
        recall = (
            len(set(mentions).intersection(set(gold_concepts))) / len(gold_concepts)
            if gold_concepts
            else 0.0
        )
        rows.append(
            {
                "example_id": r.get("example_id"),
                "pair_id": r.get("pair_id"),
                "task_type": r.get("task_type"),
                "variant_type": r.get("variant_type"),
                "prompt_type": r.get("prompt_type"),
                "model": r.get("model"),
                "gold_answer": gold,
                "parsed_answer": parsed,
                "correct": int(parsed == gold),
                "unclear": int(parsed == "unclear"),
                "concept_recall_rough": recall,
            }
        )
    return pd.DataFrame(rows)


def format_counter(c: Counter) -> str:
    return ", ".join(f"{k}: {v}" for k, v in sorted(c.items()))


def extract_run_prefix(gen_file: Path) -> str:
    name = gen_file.stem
    return name.replace("generations_", "", 1)


def load_manifest(metadata_dir: Path, run_prefix: str) -> dict | None:
    p = metadata_dir / f"run_manifest_{run_prefix}.json"
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def load_config_snapshot_text(path_str: str | None) -> str | None:
    if not path_str:
        return None
    p = Path(path_str)
    if not p.exists():
        return None
    return p.read_text(encoding="utf-8").rstrip()


def _format_hypothesis_lines(by_prompt: pd.DataFrame, flip_rate: float) -> list[str]:
    lines: list[str] = []
    if by_prompt.empty:
        return lines

    prompt_acc = {
        str(r["prompt_type"]): float(r["accuracy"])
        for _, r in by_prompt.iterrows()
        if pd.notna(r["accuracy"])
    }

    ranked = sorted(prompt_acc.items(), key=lambda x: x[1], reverse=True)
    if ranked:
        best_name, best_acc = ranked[0]
        worst_name, worst_acc = ranked[-1]
        lines.append(
            f"- Prompt-conditioned behavior hypothesis: performance dispersion across prompt framings remains large (best={best_name}:{best_acc:.3f}, worst={worst_name}:{worst_acc:.3f})."
        )

    if "mechanistic" in prompt_acc:
        lines.append(
            f"- Mechanistic-framing hypothesis: explicit mechanistic prompting may destabilize small-model reasoning in this setup (mechanistic accuracy={prompt_acc['mechanistic']:.3f})."
        )

    if "adversarial" in prompt_acc:
        lines.append(
            f"- Heuristic-discrimination hypothesis: adversarial framing may induce stronger shortcut discrimination rather than deeper causal abstraction (adversarial accuracy={prompt_acc['adversarial']:.3f})."
        )

    lines.append(
        f"- Stability hypothesis: answer flips across prompt reframing remain non-trivial (flip_rate={flip_rate:.3f}), consistent with prompt-contingent decision policy shifts."
    )
    return lines


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    results_dir = root / "results"
    gen_dir = results_dir / "generations"
    metadata_dir = results_dir / "metadata"
    report_dir = root / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    cfg_path = root / "config.yaml"
    _ = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))

    gen_files = sorted(gen_dir.glob("generations_*.jsonl"))
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append("# Experiment Trace Report")
    lines.append("")
    lines.append(f"Generated at: {now}")
    lines.append("")
    lines.append("## Current config.yaml")
    lines.append("```yaml")
    lines.append(cfg_path.read_text(encoding="utf-8").rstrip())
    lines.append("```")
    lines.append("")

    if not gen_files:
        lines.append("No generation runs found in results/generations.")
    else:
        lines.append("## Run-by-run trace")
        lines.append("")
        for gf in gen_files:
            records = read_jsonl(gf)
            if not records:
                continue
            df = score_records(records)
            run_prefix = extract_run_prefix(gf)
            manifest = load_manifest(metadata_dir, run_prefix)

            mtime = datetime.fromtimestamp(gf.stat().st_mtime).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            model_set = sorted(set(df["model"].dropna().tolist()))
            prompt_set = sorted(set(df["prompt_type"].dropna().tolist()))
            task_counts = Counter(df["task_type"].tolist())
            var_counts = Counter(df["variant_type"].tolist())

            overall_acc = df["correct"].mean()
            unclear_rate = df["unclear"].mean()
            concept_recall = df["concept_recall_rough"].mean()

            by_prompt = (
                df.groupby("prompt_type", as_index=False)
                .agg(
                    n=("example_id", "count"),
                    accuracy=("correct", "mean"),
                    unclear_rate=("unclear", "mean"),
                    concept_recall_rough=("concept_recall_rough", "mean"),
                )
                .sort_values("prompt_type")
            )

            by_variant = (
                df.groupby("variant_type", as_index=False)
                .agg(n=("example_id", "count"), accuracy=("correct", "mean"))
                .sort_values("variant_type")
            )

            ex_stability = []
            for _, g in df.groupby("example_id"):
                answers = g["parsed_answer"].tolist()
                uniq = set(answers)
                maj = max(answers.count(a) for a in uniq)
                ex_stability.append(maj / len(answers))
            mean_stability = mean(ex_stability) if ex_stability else float("nan")
            flip_rate = sum(
                1 for _, g in df.groupby("example_id") if len(set(g["parsed_answer"])) > 1
            ) / max(df["example_id"].nunique(), 1)

            lines.append(f"### {gf.name}")
            lines.append(f"- File modified: {mtime}")
            lines.append(f"- Run prefix: {run_prefix}")
            if manifest:
                lines.append(f"- Run name: {manifest.get('run_name')}")
                lines.append(f"- Config snapshot: {manifest.get('config_snapshot_path')}")
                lines.append(f"- max_new_tokens: {manifest.get('max_new_tokens')}")
                lines.append(f"- do_sample: {manifest.get('do_sample')}")
                lines.append(f"- datasets: {manifest.get('datasets')}")
                lines.append(f"- prompt_types (manifest): {manifest.get('prompt_types')}")
            else:
                lines.append("- Manifest: missing (legacy run before metadata logging).")
            lines.append(f"- Records: {len(df)}")
            lines.append(f"- Unique examples: {df['example_id'].nunique()}")
            lines.append(f"- Models in file: {model_set}")
            lines.append(f"- Prompt types observed: {prompt_set}")
            lines.append(f"- Task distribution: {format_counter(task_counts)}")
            lines.append(f"- Variant distribution: {format_counter(var_counts)}")
            lines.append(f"- Overall accuracy: {overall_acc:.4f}")
            lines.append(f"- Overall unclear_rate: {unclear_rate:.4f}")
            lines.append(f"- Overall concept_recall_rough: {concept_recall:.4f}")
            lines.append(f"- Mean prompt stability score: {mean_stability:.4f}")
            lines.append(f"- Prompt flip rate across examples: {flip_rate:.4f}")
            lines.append("")

            if manifest:
                cfg_text = load_config_snapshot_text(manifest.get("config_snapshot_path"))
                if cfg_text:
                    lines.append("Config snapshot used in this run:")
                    lines.append("```yaml")
                    lines.append(cfg_text)
                    lines.append("```")
                    lines.append("")

            lines.append("Prompt-level summary:")
            lines.append("")
            lines.append(by_prompt.to_markdown(index=False))
            lines.append("")
            lines.append("Variant-level summary:")
            lines.append("")
            lines.append(by_variant.to_markdown(index=False))
            lines.append("")

        lines.append("## Cross-run change trace")
        lines.append("")
        lines.append(
            "| run_file | run_prefix | run_name | modified_time | n_records | unique_examples | models | prompt_types | manifest |"
        )
        lines.append("|---|---|---|---:|---:|---:|---|---|---|")
        for gf in gen_files:
            records = read_jsonl(gf)
            df = score_records(records)
            run_prefix = extract_run_prefix(gf)
            manifest = load_manifest(metadata_dir, run_prefix)
            mtime = datetime.fromtimestamp(gf.stat().st_mtime).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            models = ";".join(sorted(set(df["model"].dropna().tolist())))
            prompts = ";".join(sorted(set(df["prompt_type"].dropna().tolist())))
            run_name = manifest.get("run_name") if manifest else "legacy"
            manifest_flag = "yes" if manifest else "no"
            lines.append(
                f"| {gf.name} | {run_prefix} | {run_name} | {mtime} | {len(df)} | {df['example_id'].nunique()} | {models} | {prompts} | {manifest_flag} |"
            )

        lines.append("")
        lines.append("## Traceability status")
        lines.append(
            "- New runs now support exact per-run YAML snapshots and machine-readable manifests under results/metadata/."
        )
        lines.append(
            "- Legacy runs (before this update) are still inferential unless their YAML was manually preserved elsewhere."
        )

        latest_file = gen_files[-1]
        latest_records = read_jsonl(latest_file)
        latest_df = score_records(latest_records)
        latest_by_prompt = (
            latest_df.groupby("prompt_type", as_index=False)
            .agg(accuracy=("correct", "mean"))
            .sort_values("accuracy", ascending=False)
        )
        latest_flip_rate = sum(
            1
            for _, g in latest_df.groupby("example_id")
            if len(set(g["parsed_answer"])) > 1
        ) / max(latest_df["example_id"].nunique(), 1)

        lines.append("")
        lines.append("## Scientific interpretation (auto-generated)")
        lines.append("")
        lines.append("### What this run suggests")
        lines.append(
            "- This report treats outputs as exploratory interpretability signals, not proof of internal mechanism."
        )
        lines.append(
            f"- Latest run analyzed: {latest_file.name} ({len(latest_df)} records; {latest_df['example_id'].nunique()} unique examples)."
        )
        lines.append(
            f"- Prompt-conditioned answer instability remains measurable (flip_rate={latest_flip_rate:.3f})."
        )
        lines.append("")

        lines.append("### Emerging hypotheses")
        hypo_lines = _format_hypothesis_lines(latest_by_prompt, latest_flip_rate)
        lines.extend(hypo_lines if hypo_lines else ["- Insufficient prompt-contrast data for hypothesis extraction."])
        lines.append("")

        lines.append("### What these results do NOT establish")
        lines.append("- Behavioral instability alone does not prove causal reasoning failure.")
        lines.append("- Probe separability (if later observed) would indicate recoverability, not necessity.")
        lines.append("- Hidden-state similarity or drift (if later measured) would not by itself prove mechanism equivalence.")
        lines.append("- Synthetic-toxicity benchmark performance should not be interpreted as biomedical knowledge quality.")
        lines.append("")

        lines.append("### Possible confounders and unresolved ambiguities")
        lines.append("- Prompt templates differ in instruction density and pragmatic framing; effects may mix reasoning changes with instruction-following changes.")
        lines.append("- Simple yes/no parsing may undercount nuanced or hedge-heavy outputs.")
        lines.append("- Small sample size improves control but increases variance; replication across seeds/checkpoints remains necessary.")
        lines.append("- Surface terminology effects may partially reflect tokenization/lexical familiarity rather than abstraction collapse.")
        lines.append("")

        lines.append("### Next mechanistic questions")
        lines.append("- Layerwise latent drift: which layers move most under prompt reframing for the same example?")
        lines.append("- Prompt-pair geometry: do adversarial and mechanistic prompts form separable latent clusters?")
        lines.append("- Causal-structure sensitivity: does latent drift increase more for true graph perturbations than term renaming?")
        lines.append("- Scaling trajectory: do instability and flip patterns persist across Qwen2.5 0.5B -> 1.5B -> 3B checkpoints?")
        lines.append("- Faithfulness frontier: when chain-of-thought style prompting changes text, does it align with more stable latent causal abstraction?")

    out_path = report_dir / "experiment_trace_report.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
