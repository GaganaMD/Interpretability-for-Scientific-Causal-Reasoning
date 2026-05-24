from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List

import yaml


def ensure_dir(path: Path) -> None:
    """Create directory path if it does not exist."""
    path.mkdir(parents=True, exist_ok=True)


def read_jsonl(path: Path) -> List[Dict]:
    """Read JSONL file into list of dicts."""
    records = []
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def write_jsonl(path: Path, records: Iterable[Dict]) -> None:
    """Write iterable of dicts to JSONL."""
    ensure_dir(path.parent)
    with path.open('w', encoding='utf-8') as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')


def load_config(path: Path) -> Dict:
    """Load YAML config file."""
    with path.open('r', encoding='utf-8') as f:
        return yaml.safe_load(f)
