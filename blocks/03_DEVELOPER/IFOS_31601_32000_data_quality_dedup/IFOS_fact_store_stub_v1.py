# IFOS Fact Store Stub v1
from __future__ import annotations
from typing import Dict, Any, List, Optional
import datetime

class FactStore:
    def __init__(self) -> None:
        self.facts: Dict[str, Dict[str, Any]] = {}
        self.versions: Dict[str, List[Dict[str, Any]]] = {}

    def upsert_fact(self, fact_id: str, fact: Dict[str, Any]) -> None:
        self.facts[fact_id]=fact

    def add_version(self, fact_id: str, value: Any, source_id: str, confidence: float, evidence_ids: List[str]) -> Dict[str, Any]:
        fv_id=f"fv.{len(self.versions.get(fact_id,[]))+1:06d}"
        now=datetime.datetime.utcnow().isoformat()+"Z"
        fv={"fact_version_id":fv_id,"fact_id":fact_id,"value":value,"valid_from":now,"valid_to":None,
            "observed_at":now,"source_id":source_id,"confidence":confidence,"evidence_ids":evidence_ids,"version":"1.0.0"}
        self.versions.setdefault(fact_id,[]).append(fv)
        return fv

    def current_value(self, fact_id: str) -> Optional[Any]:
        vs=self.versions.get(fact_id,[])
        if not vs: return None
        return max(vs, key=lambda x: (x.get("confidence",0), x.get("observed_at",""))).get("value")
