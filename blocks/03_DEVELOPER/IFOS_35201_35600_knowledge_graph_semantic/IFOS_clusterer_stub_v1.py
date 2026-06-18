# IFOS Clusterer Stub v1
from __future__ import annotations
from typing import List, Dict, Any
import random

def cluster(members: List[str], k: int=3) -> List[Dict[str, Any]]:
    # Stub: replace with k-means / hdbscan
    random.shuffle(members)
    buckets=[members[i::k] for i in range(k)]
    return [{"cluster_id":f"cl.{i}", "members":b} for i,b in enumerate(buckets)]
