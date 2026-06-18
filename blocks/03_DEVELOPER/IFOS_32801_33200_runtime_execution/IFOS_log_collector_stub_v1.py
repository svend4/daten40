# IFOS Log Collector Stub v1
from __future__ import annotations
from typing import Dict, Any
import datetime

class LogCollector:
    def __init__(self) -> None:
        self.entries=[]

    def _add(self, run_id: str, level: str, msg: str, fields: Dict[str, Any] | None=None) -> None:
        self.entries.append({
            "run_id": run_id,
            "level": level,
            "message": msg,
            "ts": datetime.datetime.utcnow().isoformat()+"Z",
            "fields": fields or {},
            "redacted": True,
        })

    def info(self, run_id: str, msg: str, fields: Dict[str, Any] | None=None) -> None:
        self._add(run_id, "info", msg, fields)

    def warn(self, run_id: str, msg: str, fields: Dict[str, Any] | None=None) -> None:
        self._add(run_id, "warn", msg, fields)

    def error(self, run_id: str, msg: str, fields: Dict[str, Any] | None=None) -> None:
        self._add(run_id, "error", msg, fields)
