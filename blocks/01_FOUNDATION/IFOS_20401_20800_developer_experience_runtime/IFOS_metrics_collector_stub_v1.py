# IFOS Metrics Collector Stub v1
from __future__ import annotations
from typing import Dict

class Metrics:
    def __init__(self) -> None:
        self.counters: Dict[str, float] = {}
        self.timers: Dict[str, float] = {}

    def inc(self, name: str, value: float = 1.0) -> None:
        self.counters[name] = self.counters.get(name, 0.0) + value

    def observe_ms(self, name: str, ms: float) -> None:
        self.timers[name] = ms
