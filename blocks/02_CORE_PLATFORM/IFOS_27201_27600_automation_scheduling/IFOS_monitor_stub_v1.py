# IFOS Monitor Stub v1
from __future__ import annotations
from typing import Dict, Any, List
import time

def evaluate_no_success(runs: List[Dict[str, Any]], job_id: str, threshold_seconds: int) -> bool:
    now = time.time()
    successes = [r for r in runs if r.get("job_id")==job_id and r.get("status")=="succeeded"]
    if not successes:
        # if there were any runs at all, check last run age; otherwise treat as breach
        any_runs = [r for r in runs if r.get("job_id")==job_id]
        if not any_runs:
            return True
        last_ts = max(r.get("finished_at_ts", 0) for r in any_runs)
        return (now - last_ts) > threshold_seconds
    last_success = max(r.get("finished_at_ts", 0) for r in successes)
    return (now - last_success) > threshold_seconds
