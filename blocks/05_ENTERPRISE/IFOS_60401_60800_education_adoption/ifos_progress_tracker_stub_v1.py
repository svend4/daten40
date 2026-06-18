# ifos_progress_tracker_stub_v1.py
from __future__ import annotations
from typing import Dict

def update(progress: Dict, event: str) -> Dict:
    progress.setdefault("events", []).append(event)
    return progress
