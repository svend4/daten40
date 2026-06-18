# IFOS Normalizer Stub v1
from __future__ import annotations
from typing import Dict, Any
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

STRIP_PARAMS = {"utm_source","utm_medium","utm_campaign","utm_term","utm_content"}

def canonicalize_url(url: str) -> str:
    p=urlparse(url)
    netloc=p.netloc.lower()
    path=p.path.rstrip("/")
    qs=[(k,v) for k,v in parse_qsl(p.query, keep_blank_values=True) if k not in STRIP_PARAMS]
    query=urlencode(qs, doseq=True)
    scheme=p.scheme if p.scheme else "https"
    return urlunparse((scheme, netloc, path, "", query, ""))

def normalize_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    title=(raw.get("title") or "").strip()
    url=canonicalize_url(raw.get("url") or "")
    text=(raw.get("text") or "").strip()
    published_at=raw.get("published_at") or "1970-01-01T00:00:00Z"
    return {
        "canonical_title": title,
        "canonical_url": url,
        "content_text": text,
        "published_at": published_at,
        "language": raw.get("language","unknown"),
        "tags": raw.get("tags",[]),
    }
