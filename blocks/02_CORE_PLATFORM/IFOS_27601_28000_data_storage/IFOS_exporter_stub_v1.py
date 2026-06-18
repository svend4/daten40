# IFOS Exporter Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import json, csv, io, zipfile

def export_json(records: List[Dict[str, Any]]) -> bytes:
    return json.dumps(records, ensure_ascii=False, indent=2).encode("utf-8")

def export_csv(records: List[Dict[str, Any]], columns: List[str]) -> bytes:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=columns)
    w.writeheader()
    for r in records:
        w.writerow({c: r.get(c, "") for c in columns})
    return buf.getvalue().encode("utf-8")

def export_bundle(files: Dict[str, bytes]) -> bytes:
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path, data in files.items():
            z.writestr(path, data)
    return out.getvalue()
