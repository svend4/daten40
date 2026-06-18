# IFOS KB Ingest Pipeline Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List
import re

def redact(text: str) -> str:
    # MVP redaction: emails + long tokens
    t = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "***EMAIL***", text or "")
    t = re.sub(r"([0-9]{9}:[A-Za-z0-9_-]{20,})", "***TOKEN***", t)
    return t

def chunk_md(md: str, max_chars: int=1200) -> List[str]:
    md = md or ""
    parts = []
    cur = ""
    for line in md.splitlines():
        if len(cur) + len(line) + 1 > max_chars:
            parts.append(cur)
            cur = ""
        cur += line + "\n"
    if cur.strip():
        parts.append(cur)
    return parts

def ingest_artifacts(artifacts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Returns chunks with metadata (for keyword index or vector store)
    out = []
    for a in artifacts or []:
        kind = a.get("kind","")
        content = a.get("content","")
        if kind in ("logs","incident"):
            content = redact(content)
        chunks = chunk_md(content) if kind in ("md","doc") else [json.dumps(a, ensure_ascii=False)]
        for i, ch in enumerate(chunks):
            out.append({"id":f"{a.get('id','')}.{i}", "kind":kind, "text":ch, "meta":a.get("meta",{})})
    return out
