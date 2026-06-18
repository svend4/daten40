# ifos_abuse_detector_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def detect(review: Dict) -> List[str]:
    signals=[]
    text=" ".join(review.get("pros",[])+review.get("cons",[])).lower()
    if "http" in text: signals.append("links_present")
    if review.get("ttfv_minutes",0)==0 and review.get("rating",0)==5: signals.append("too_good_to_be_true")
    return signals
