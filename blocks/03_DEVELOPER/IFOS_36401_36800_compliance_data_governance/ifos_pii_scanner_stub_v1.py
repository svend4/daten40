# ifos_pii_scanner_stub_v1.py
from __future__ import annotations
import re
from typing import Dict, Any, List

EMAIL=re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE=re.compile(r"\+?\d[\d\s\-()]{7,}\d")

def scan(text: str) -> List[Dict[str, Any]]:
    findings=[]
    for m in EMAIL.finditer(text):
        findings.append({"label":"pii.email","start":m.start(),"end":m.end()})
    for m in PHONE.finditer(text):
        findings.append({"label":"pii.phone","start":m.start(),"end":m.end()})
    return findings

def mask(text: str, findings: List[Dict[str, Any]]) -> str:
    # naive masking: replace spans from end to start
    out=text
    for f in sorted(findings, key=lambda x: x["start"], reverse=True):
        out=out[:f["start"]] + "***" + out[f["end"]:]
    return out
