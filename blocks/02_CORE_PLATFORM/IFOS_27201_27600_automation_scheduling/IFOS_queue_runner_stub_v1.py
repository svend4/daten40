# IFOS Queue Runner Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def enqueue(queue: List[Dict[str, Any]], run: Dict[str, Any]) -> None:
    queue.append(run)

def dequeue(queue: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    if not queue:
        return None
    return queue.pop(0)
