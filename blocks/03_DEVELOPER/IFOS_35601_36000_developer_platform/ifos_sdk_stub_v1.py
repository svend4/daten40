# ifos_sdk_stub_v1.py
from __future__ import annotations
from typing import Dict, Any
import requests

def http_get(url: str, headers: Dict[str,str] | None=None, timeout: float=10.0) -> Dict[str, Any]:
    r=requests.get(url, headers=headers or {}, timeout=timeout)
    return {"status_code": r.status_code, "text": r.text}
