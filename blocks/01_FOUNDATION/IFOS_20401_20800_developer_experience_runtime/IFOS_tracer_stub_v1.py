# IFOS Tracer Stub v1
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List
import time

@dataclass
class Span:
    name: str
    step_id: str
    start: float
    end: float = 0.0
    attrs: Dict[str, Any] = None

def start_span(name: str, step_id: str, attrs: Dict[str, Any] | None = None) -> Span:
    return Span(name=name, step_id=step_id, start=time.time(), attrs=attrs or {})

def end_span(span: Span) -> Span:
    span.end = time.time()
    return span
