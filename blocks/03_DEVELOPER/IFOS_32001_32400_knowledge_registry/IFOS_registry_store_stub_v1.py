# IFOS Registry Store Stub v1
from __future__ import annotations
from typing import Dict, Any, List, Optional

class RegistryStore:
    def __init__(self) -> None:
        self.items: Dict[str, Dict[str, Any]] = {}
        self.taxonomy: Dict[str, Dict[str, Any]] = {}
        self.reviews: Dict[str, Dict[str, Any]] = {}
        self.signals: Dict[str, List[Dict[str, Any]]] = {}

    def upsert_item(self, item: Dict[str, Any]) -> None:
        self.items[item["id"]] = item

    def get_item(self, item_id: str) -> Optional[Dict[str, Any]]:
        return self.items.get(item_id)

    def list_items(self) -> List[Dict[str, Any]]:
        return list(self.items.values())

    def add_review(self, review: Dict[str, Any]) -> None:
        self.reviews[review["review_id"]] = review

    def add_trust_signal(self, signal: Dict[str, Any]) -> None:
        self.signals.setdefault(signal["item_id"], []).append(signal)
