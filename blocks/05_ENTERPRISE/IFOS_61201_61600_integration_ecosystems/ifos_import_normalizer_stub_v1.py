# ifos_import_normalizer_stub_v1.py
from __future__ import annotations
from typing import Dict

SYNONYMS={"gsheets":"google_sheets","g sheets":"google_sheets","google sheet":"google_sheets"}

def normalize_deps(asset: Dict) -> Dict:
    deps=[SYNONYMS.get(d.lower(), d) for d in asset.get("deps", [])]
    asset["deps"]=sorted(set(deps))
    return asset
