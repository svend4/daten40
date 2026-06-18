# ifos_dlp_scanner_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def scan(text: str, policy: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Stub: pretend to find email
    findings=[]
    if "@" in text:
        findings.append({"pattern":"EMAIL","action":"allow"})
    return findings
