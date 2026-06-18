# ifos_chunker_stub_v1.py
from __future__ import annotations
from typing import List, Dict

def chunk(text: str, max_chars: int = 800, overlap: int = 80) -> List[Dict]:
    chunks=[]
    i=0
    while i < len(text):
        start=i
        end=min(len(text), i+max_chars)
        chunks.append({"start":start,"end":end,"text":text[start:end]})
        i=end-overlap if end < len(text) else end
    return chunks
