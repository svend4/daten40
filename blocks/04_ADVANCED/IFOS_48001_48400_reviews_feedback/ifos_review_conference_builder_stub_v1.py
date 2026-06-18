# ifos_review_conference_builder_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def build(target_id: str, reviews: List[Dict]) -> Dict:
    return {
        "agenda":["Качество","Цена","Поддержка"],
        "briefing":"Сводка отзывов (stub)",
        "facts":[{"k":"count","v":len(reviews)}],
        "decisions":["Подходит для...","Не подходит если..."],
        "exports":["html","pdf"]
    }
