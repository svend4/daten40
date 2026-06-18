# ifos_anti_spam_fee_stub_v1.py
from __future__ import annotations

def listing_fee(doc_score: float, crash_rate: float) -> float:
    # Worse docs and higher crash rate => higher fee
    base=5.0
    fee = base * (1.0 + (1.0-doc_score) + crash_rate*2.0)
    return max(base, fee)
