from __future__ import annotations

import argparse
from pathlib import Path

import torch
from tqdm import tqdm

from load_model import load_model_and_tokenizer
from prompts import build_prompt
from utils import load_config, read_jsonl, ensure_dir


def main() -> None:
    parser = argparse.ArgumentParser(description='Collect hidden-state representations (no text generation).')
    parser.add_argument('--config', type=str, default='config.yaml')
    parser.add_argument('--prompt_type', type=str, default=None)
    args = parser.parse_args()

    cfg = load_config(Path(args.config))
    prompt_type = args.prompt_type or cfg.get('hidden_states', {}).get('prompt_type', 'mechanistic')

    tokenizer, model = load_model_and_tokenizer(cfg['model_name'])
    examples = []
    for ds in cfg['datasets']:
        examples.extend(read_jsonl(Path(ds)))

    records = []
    for ex in tqdm(examples, desc='Collecting activations'):
        prompt = build_prompt(ex, prompt_type)
        messages = [{'role': 'user', 'content': prompt}]
        inp = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors='pt').to(model.device)
        with torch.no_grad():
            out = model(inp, output_hidden_states=True)
        hs = out.hidden_states
        final_token = [h[0, -1, :].detach().cpu() for h in hs]
        mean_pool = [h[0].mean(dim=0).detach().cpu() for h in hs]
        records.append({
            'example_id': ex['id'],
            'pair_id': ex['pair_id'],
            'task_type': ex['task_type'],
            'variant_type': ex['variant_type'],
            'gold_answer': ex['gold_answer'],
            'gold_concepts': ex['gold_concepts'],
            'final_token_by_layer': final_token,
            'mean_pool_by_layer': mean_pool,
        })

    out_dir = Path(cfg.get('output_dir', 'results')) / 'activations'
    ensure_dir(out_dir)
    out_path = out_dir / 'qwen2p5_hidden_states.pt'
    torch.save({'model_name': cfg['model_name'], 'prompt_type': prompt_type, 'records': records}, out_path)
    print(f'Saved hidden states for {len(records)} examples to {out_path}')


if __name__ == '__main__':
    main()
