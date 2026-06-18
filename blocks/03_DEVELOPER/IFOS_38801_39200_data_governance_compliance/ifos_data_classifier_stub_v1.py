# ifos_data_classifier_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def classify(resource: Dict[str, Any], sample: str) -> Dict[str, Any]:
    # Stub: naive classification example
    tags=[]
    if "@" in sample: tags.append("PII:EMAIL")
    if "DE" in sample and len(sample) > 15: tags.append("FIN:IBAN?")
    level="CONFIDENTIAL" if tags else "INTERNAL"
    return {"level": level, "tags": tags}
