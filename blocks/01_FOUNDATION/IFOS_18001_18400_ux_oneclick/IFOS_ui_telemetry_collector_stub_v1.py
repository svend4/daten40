# IFOS UI Telemetry Collector Stub v1
from __future__ import annotations
from typing import Dict, Any
import json

def ingest_event(path: str, event: Dict[str, Any]) -> None:
    with open(path,"a",encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
