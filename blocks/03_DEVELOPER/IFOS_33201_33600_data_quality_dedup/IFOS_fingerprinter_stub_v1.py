# IFOS Fingerprinter Stub v1
from __future__ import annotations
from typing import Dict, Any
import re
import hashlib

def norm_url(url: str) -> str:
    url=url.lower().strip()
    url=re.sub(r"^https?://", "", url)
    url=url.rstrip("/")
    return url

def fp_value(kind: str, value: str) -> str:
    data=f"{kind}:{value}".encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def fingerprints(canon: Dict[str, Any]) -> Dict[str, str]:
    fps={}
    title=canon.get("title","").lower()
    fps["name"]=fp_value("name", title)
    url=canon.get("url")
    if url:
        fps["url"]=fp_value("url", norm_url(url))
    return fps
