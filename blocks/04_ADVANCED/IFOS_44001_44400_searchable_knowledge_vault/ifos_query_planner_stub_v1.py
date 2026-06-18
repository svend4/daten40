# ifos_query_planner_stub_v1.py
from __future__ import annotations

def plan(mode: str, top_k: int = 50) -> dict:
    if mode == "fulltext":
        return {"steps":[{"op":"fulltext_candidate","k":top_k*4},{"op":"rank","k":top_k}]}
    if mode == "semantic":
        return {"steps":[{"op":"semantic_candidate","k":top_k*4},{"op":"rank","k":top_k}]}
    return {"steps":[{"op":"fulltext_candidate","k":top_k*4},{"op":"semantic_candidate","k":top_k*4},{"op":"merge","strategy":"rrf"},{"op":"rank","k":top_k}]}
