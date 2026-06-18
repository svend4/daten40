# ifos_retry_policy_stub_v1.py
from __future__ import annotations
import random, time
from typing import Callable, Any

RETRYABLE={429,500,502,503,504}

def with_retry(fn: Callable[[],Any], max_attempts:int=5, base:float=0.5):
    for i in range(1, max_attempts+1):
        res=fn()
        status=getattr(res,"get",lambda k,default=None: None)("status",None) if isinstance(res,dict) else None
        if status is None or status not in RETRYABLE:
            return res
        sleep=base*(2**(i-1))*(1+random.random()*0.2)
        time.sleep(min(10,sleep))
    return res
