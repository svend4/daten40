# ifos_kw_doc_model_stub_v1.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Document:
    doc_id: str
    doc_type: str
    title: str
    body: str
    meta: Dict = field(default_factory=dict)
    links: List[str] = field(default_factory=list)
