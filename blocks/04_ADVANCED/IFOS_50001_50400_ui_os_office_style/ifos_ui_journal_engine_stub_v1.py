# ifos_ui_journal_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def append(journal: Dict, entry: Dict) -> Dict:
    journal.setdefault("entries",[]).append(entry)
    return journal
