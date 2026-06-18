# ifos_change_release_train_stub_v1.py
from __future__ import annotations
from datetime import date, timedelta

def next_weekly_release(d: date, weekday: int = 4) -> date:
    # weekday: 0=Mon ... 4=Fri
    delta=(weekday - d.weekday()) % 7
    return d + timedelta(days=delta)
