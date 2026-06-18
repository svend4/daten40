# IFOS Fingerprinter Stub v1
from __future__ import annotations
from typing import List
import hashlib

def _sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def fp_exact_url(canonical_url: str) -> str:
    return "fp:exact_url:" + _sha256(canonical_url)[:16]

def fp_title_day(title: str, day: str) -> str:
    return "fp:title_day:" + _sha256(title.lower().strip() + "|" + day)[:16]

def fp_text_signature(text: str) -> str:
    # Placeholder: stable signature; replace with simhash/minhash later
    return "fp:text_sig:" + _sha256(text.lower().strip())[:16]

def build_fingerprints(canonical_url: str, title: str, day: str, text: str) -> List[str]:
    return [fp_exact_url(canonical_url), fp_title_day(title, day), fp_text_signature(text)]
