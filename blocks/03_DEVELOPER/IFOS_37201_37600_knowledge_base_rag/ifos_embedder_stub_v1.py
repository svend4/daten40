# ifos_embedder_stub_v1.py
from __future__ import annotations
from typing import List
import math

def embed(text: str, dim: int = 16) -> List[float]:
    # Stub embedding: deterministic toy vector from character codes
    v=[0.0]*dim
    for i,ch in enumerate(text[:2048]):
        v[i % dim] += (ord(ch) % 31) / 31.0
    # L2 normalize
    n=math.sqrt(sum(x*x for x in v)) or 1.0
    return [x/n for x in v]
