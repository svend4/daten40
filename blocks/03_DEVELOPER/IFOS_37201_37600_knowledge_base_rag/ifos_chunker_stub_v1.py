# ifos_chunker_stub_v1.py
from __future__ import annotations
from typing import Dict, Any, List

def chunk_text(text: str, target_chars: int = 1200, overlap: int = 120) -> List[Dict[str, Any]]:
    chunks=[]
    i=0
    while i < len(text):
        j=min(len(text), i+target_chars)
        chunk=text[i:j]
        chunks.append({"text":chunk, "offsets":{"start":i,"end":j}})
        i=max(j-overlap, j)
    return chunks
