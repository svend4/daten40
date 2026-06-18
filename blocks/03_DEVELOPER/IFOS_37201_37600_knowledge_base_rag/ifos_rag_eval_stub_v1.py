# ifos_rag_eval_stub_v1.py
from __future__ import annotations
from typing import List, Dict, Any

def eval_recall_at_k(gold: List[str], retrieved: List[str], k: int) -> float:
    hit=0
    for g in gold:
        if g in retrieved[:k]:
            hit += 1
    return hit / max(1, len(gold))

def run_eval(gold_chunks: List[str], retrieved_chunks: List[str]) -> Dict[str, Any]:
    return {"recall_at_5": eval_recall_at_k(gold_chunks, retrieved_chunks, 5)}
