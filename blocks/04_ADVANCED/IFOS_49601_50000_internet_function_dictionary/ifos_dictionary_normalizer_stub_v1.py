# ifos_dictionary_normalizer_stub_v1.py
from __future__ import annotations
from typing import Dict

def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())
