# ifos_ratelimit_bucket_stub_v1.py
from __future__ import annotations
import time

class TokenBucket:
    def __init__(self, capacity:int, refill_per_sec:float):
        self.capacity=capacity
        self.tokens=float(capacity)
        self.refill_per_sec=refill_per_sec
        self.last=time.time()
    def take(self, n:int=1) -> bool:
        now=time.time()
        self.tokens=min(self.capacity, self.tokens+(now-self.last)*self.refill_per_sec)
        self.last=now
        if self.tokens>=n:
            self.tokens-=n
            return True
        return False
