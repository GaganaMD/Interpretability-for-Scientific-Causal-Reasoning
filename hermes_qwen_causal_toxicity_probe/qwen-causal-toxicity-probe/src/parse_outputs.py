from __future__ import annotations

import re
from typing import List


def parse_yes_no(text: str) -> str:
    """Parse answer into yes/no/unclear using simple transparent rules."""
    t = text.strip().lower()
    yes_match = re.search(r'\byes\b', t)
    no_match = re.search(r'\bno\b', t)
    if yes_match and no_match:
        return 'yes' if yes_match.start() < no_match.start() else 'no'
    if yes_match:
        return 'yes'
    if no_match:
        return 'no'
    return 'unclear'


CONCEPT_PATTERNS = {
    'confounding': [r'confound', r'shared cause', r'common cause'],
    'mediation': [r'mediator', r'mediation', r'intermediate'],
    'selection_bias': [r'selection bias', r'selected sample', r'conditioning on'],
    'collider': [r'collider'],
    'randomization': [r'randomi[sz]ed', r'random assignment'],
    'observational association': [r'observational', r'association', r'correlation'],
    'mechanism': [r'mechanis', r'biological pathway', r'causal chain'],
    'adverse outcome': [r'adverse', r'toxic', r'injury', r'outcome'],
}


def concept_mentions(text: str) -> List[str]:
    """Return rough concept mentions based on keyword patterns."""
    t = text.lower()
    found = []
    for concept, pats in CONCEPT_PATTERNS.items():
        if any(re.search(p, t) for p in pats):
            found.append(concept)
    return found
