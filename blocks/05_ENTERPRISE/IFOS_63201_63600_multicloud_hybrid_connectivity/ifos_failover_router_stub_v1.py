# ifos_failover_router_stub_v1.py
from __future__ import annotations
import random, time
PRIMARY="env.prod.eu"
SECONDARY="env.prod.eu.alt"
def choose():
    # placeholder health check
    primary_ok = random.random() > 0.1
    return PRIMARY if primary_ok else SECONDARY
if __name__ == "__main__":
    for _ in range(5):
        print("route_to:", choose())
        time.sleep(0.2)
