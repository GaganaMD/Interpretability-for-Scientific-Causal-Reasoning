from __future__ import annotations

from typing import Tuple

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def load_model_and_tokenizer(model_name: str = 'Qwen/Qwen2.5-0.5B-Instruct') -> Tuple[AutoTokenizer, AutoModelForCausalLM]:
    """Load tokenizer/model with CPU/GPU-safe defaults and hidden state outputs enabled."""
    has_cuda = torch.cuda.is_available()
    dtype = torch.float16 if has_cuda else torch.float32
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        trust_remote_code=True,
        torch_dtype=dtype,
        device_map='auto',
    )
    model.config.output_hidden_states = True
    model.eval()
    return tokenizer, model
