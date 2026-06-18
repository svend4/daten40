# ifos_pii_detector_stub_v1.py
from __future__ import annotations
import re
from typing import Dict, Any, List

EMAIL=re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE=re.compile(r"\+?\d[\d\s\-]{7,}\d")

def detect(text: str) -> Dict[str, List[str]]:
    return {"email": EMAIL.findall(text), "phone": PHONE.findall(text)}
