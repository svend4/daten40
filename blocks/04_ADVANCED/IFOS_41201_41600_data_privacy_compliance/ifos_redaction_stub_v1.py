# ifos_redaction_stub_v1.py
from __future__ import annotations
import re

def mask_email(text: str) -> str:
    return re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "<email_redacted>", text)

def mask_phone_keep_last4(text: str) -> str:
    def repl(m):
        s=m.group(0)
        digits=re.sub(r"\D","",s)
        return "<phone_redacted_****"+digits[-4:]+">" if len(digits)>=4 else "<phone_redacted>"
    return re.sub(r"\+?\d[\d\s\-]{7,}\d", repl, text)
