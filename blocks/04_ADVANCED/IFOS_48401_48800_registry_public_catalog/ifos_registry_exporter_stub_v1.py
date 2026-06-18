# ifos_registry_exporter_stub_v1.py
from __future__ import annotations
from typing import Dict, List
import csv, io

def export_csv(items: List[Dict]) -> str:
    out=io.StringIO()
    w=csv.writer(out)
    w.writerow(["item_id","name","item_type","license"])
    for i in items:
        w.writerow([i.get("item_id"), i.get("name"), i.get("item_type"), i.get("license")])
    return out.getvalue()
