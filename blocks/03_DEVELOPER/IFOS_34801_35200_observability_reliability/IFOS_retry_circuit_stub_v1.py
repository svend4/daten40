# IFOS Retry + Circuit Breaker Stub v1
from __future__ import annotations
from typing import Callable, Any
import time, random

def with_retry(fn: Callable[[], Any], max_attempts: int=3, base_delay: float=0.2) -> Any:
    attempt=0
    while True:
        attempt += 1
        try:
            return fn()
        except Exception as e:
            if attempt >= max_attempts:
                raise
            delay = base_delay * (2 ** (attempt-1)) * (1 + random.random()*0.3)
            time.sleep(delay)
