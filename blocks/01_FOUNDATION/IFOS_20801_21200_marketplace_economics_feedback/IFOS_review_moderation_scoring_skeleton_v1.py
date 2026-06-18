# IFOS Review Moderation & Scoring Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List
import re

def is_spam(text: str) -> bool:
    return bool(re.search(r"(free money|click here|subscribe now)", text.lower()))

def moderate(review: Dict[str, Any]) -> Dict[str, Any]:
    text = " ".join([review.get("text", {}).get("pros",""), review.get("text", {}).get("cons",""), review.get("text", {}).get("notes","")])
    if is_spam(text):
        review["moderation"]={"status":"rejected","reasons":["spam_pattern"]}
    else:
        review["moderation"]={"status":"approved","reasons":[]}
    return review

def verified_weight(review: Dict[str, Any]) -> float:
    return 1.0 if review.get("author", {}).get("verified_usage") else 0.4

def aggregate(reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
    ratings=[]
    weights=[]
    for r in reviews:
        if r.get("moderation", {}).get("status") != "approved":
            continue
        ratings.append(r["rating"])
        weights.append(verified_weight(r))
    if not ratings:
        return {"count":0,"mean":0,"median":0,"confidence":0}
    wsum=sum(weights)
    mean=sum(rt*w for rt,w in zip(ratings,weights))/wsum
    median=sorted(ratings)[len(ratings)//2]
    confidence=min(1.0, (len(ratings)/20.0) * (wsum/len(ratings)))
    return {"count":len(ratings),"mean":mean,"median":median,"confidence":confidence}
