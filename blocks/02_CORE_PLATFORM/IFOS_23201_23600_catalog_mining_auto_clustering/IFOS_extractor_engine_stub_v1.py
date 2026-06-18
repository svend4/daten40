# IFOS Extractor Engine Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def extract_atoms(normalized: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Stub: normalized should include nodes/edges.
    atoms=[]
    for n in normalized.get("nodes", []):
        atoms.append({
            "atom_id":"atom."+n.get("id","x"),
            "action":n.get("action","unknown"),
            "title":n.get("title", n.get("action","unknown")),
            "inputs":n.get("inputs", []),
            "outputs":n.get("outputs", []),
            "deps":n.get("deps", []),
            "constraints":n.get("constraints", {}),
            "cost_model":n.get("cost_model", {}),
            "sources":[normalized.get("source_id","")],
            "updated_at":normalized.get("ts",""),
            "version":"1.0.0",
        })
    return atoms
