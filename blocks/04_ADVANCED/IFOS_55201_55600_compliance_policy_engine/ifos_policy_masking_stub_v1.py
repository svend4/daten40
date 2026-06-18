# ifos_policy_masking_stub_v1.py
from __future__ import annotations
import re

EMAIL=re.compile(r"([\w.%-]+)@([\w.-]+)")
PHONE=re.compile(r"\+?\d[\d\s\-()]{7,}")

def mask_basic(text: str) -> str:
    text=EMAIL.sub(r"***@\2", text)
    text=PHONE.sub("***PHONE***", text)
    return text
