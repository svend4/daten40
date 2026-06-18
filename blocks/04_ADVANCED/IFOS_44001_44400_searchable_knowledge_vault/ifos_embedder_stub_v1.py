# ifos_embedder_stub_v1.py
from __future__ import annotations
from typing import List, Dict

def embed(chunks: List[Dict], model_id: str) -> List[Dict]:
    # stub: no real vectors, only refs
    out=[]
    for c in chunks:
        out.append({"chunk_range":[c["start"],c["end"]],"model_id":model_id,"vector_ref":"vector://stub"})
    return out
