# IFOS Vector Index Stub v1
from __future__ import annotations
from typing import Dict, Any, List, Tuple
import math

VECTORS: Dict[str, List[float]]={}

def upsert(object_ref: str, vec: List[float]) -> None:
    VECTORS[object_ref]=vec

def cosine(a: List[float], b: List[float]) -> float:
    dot=sum(x*y for x,y in zip(a,b))
    na=math.sqrt(sum(x*x for x in a))
    nb=math.sqrt(sum(y*y for y in b))
    if na==0 or nb==0: return 0.0
    return dot/(na*nb)

def search(query_vec: List[float], top_k: int=5) -> List[Tuple[str,float]]:
    scored=[(ref, cosine(query_vec, vec)) for ref, vec in VECTORS.items()]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]
