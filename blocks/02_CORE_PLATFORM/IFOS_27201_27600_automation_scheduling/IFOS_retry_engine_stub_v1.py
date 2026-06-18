# IFOS Retry Engine Stub v1
from __future__ import annotations
from typing import Dict, Any
import random, time

def next_delay_seconds(attempt: int, policy: Dict[str, Any]) -> float:
    backoff = policy.get("backoff", {})
    kind = backoff.get("kind", "none")
    base = float(backoff.get("base_seconds", 0))
    maxs = float(backoff.get("max_seconds", base))
    jitter = bool(backoff.get("jitter", False))
    if kind == "none":
        d = 0.0
    elif kind == "linear":
        d = base * attempt
    else:  # exponential
        d = base * (2 ** (attempt - 1))
    d = min(d, maxs)
    if jitter and d > 0:
        d = d * (0.5 + random.random())
    return d
