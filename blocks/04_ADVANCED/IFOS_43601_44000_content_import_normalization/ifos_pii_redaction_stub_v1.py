# ifos_pii_redaction_stub_v1.py
from __future__ import annotations
import re
from typing import Tuple, List, Dict

EMAIL=re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE=re.compile(r"\+?\d[\d\s\-()]{7,}\d")

def redact(text: str) -> Tuple[str, List[Dict]]:
    redactions=[]
    def sub_email(m):
        redactions.append({"type":"email","value":m.group(0)})
        return "[email]"
    def sub_phone(m):
        redactions.append({"type":"phone","value":m.group(0)})
        return "[phone]"
    t=EMAIL.sub(sub_email, text)
    t=PHONE.sub(sub_phone, t)
    return t, redactions
