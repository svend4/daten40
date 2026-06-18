# IFOS Deduper Stub v1
from __future__ import annotations
from typing import Dict, Any
import difflib

def similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(a=a.lower(), b=b.lower()).ratio()

def decide_dedupe(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    url_equal = a.get("canonical_url") == b.get("canonical_url")
    title_sim = similarity(a.get("canonical_title",""), b.get("canonical_title",""))
    text_sim = similarity(a.get("content_text","")[:2000], b.get("content_text","")[:2000])
    score = 0.0
    score += 0.5 if url_equal else 0.0
    score += 0.25 * title_sim
    score += 0.25 * text_sim
    decision = "same" if score >= 0.85 else "different" if score <= 0.6 else "unsure"
    return {"decision": decision, "score": round(score, 3), "signals":{"url_equal":url_equal,"title_sim":round(title_sim,3),"text_sim":round(text_sim,3)}}
