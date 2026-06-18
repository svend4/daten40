# ifos_rss_ingestor_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def fetch_rss(feed_url: str) -> List[Dict]:
    # stub: returns list of entries as dicts
    return [{"url":"https://example.com/a","title":"A","published_at":"2026-01-03T12:00:00Z","topic_key":"a","source":feed_url}]
