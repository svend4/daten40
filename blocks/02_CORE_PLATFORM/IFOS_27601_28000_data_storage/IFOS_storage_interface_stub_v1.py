# IFOS Storage Interface Stub v1
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Optional, Dict, Any, Iterable

class Storage(Protocol):
    def put_bytes(self, uri: str, data: bytes) -> None: ...
    def get_bytes(self, uri: str) -> bytes: ...
    def list(self, prefix: str) -> Iterable[str]: ...

def build_uri(scope: str, *parts: str) -> str:
    # Example: artifact://runs/run123/report.md
    return f"{scope}://" + "/".join(p.strip("/") for p in parts)
