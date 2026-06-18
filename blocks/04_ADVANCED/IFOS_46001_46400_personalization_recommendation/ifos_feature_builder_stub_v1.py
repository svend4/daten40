# ifos_feature_builder_stub_v1.py
from __future__ import annotations
from typing import Dict

def build_features(item: Dict, context: Dict) -> Dict:
    # stub: minimal features
    return {
        "quality": float(item.get("quality",0.5)),
        "compat": float(item.get("compat",0.5)),
        "cost": float(item.get("cost_score",0.5)),
        "setup": float(item.get("setup_score",0.5)),
        "risk": float(item.get("risk_score",0.5)),
    }
