# ifos_locale_formatting_stub_v1.py
from __future__ import annotations
from datetime import datetime

def format_date(dt: datetime, fmt: str) -> str:
    # naive placeholder
    return dt.strftime("%d.%m.%Y") if fmt=="DD.MM.YYYY" else dt.isoformat()
