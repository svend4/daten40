# ifos_test_data_generator_stub_v1.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
import random

@dataclass
class GeneratorConfig:
    seed: int = 42
    locale: str = "de-DE"

def gen_people(cfg: GeneratorConfig, count: int = 10) -> List[Dict]:
    rnd = random.Random(cfg.seed)
    out = []
    for i in range(count):
        out.append({"id": f"person_{i+1}", "name": f"Test User {rnd.randint(1000,9999)}"})
    return out
