
"""Evidence Freshness Engine — skeleton.

Inputs:
- evidence requirements catalog (CSV)
- evidence registry query client (stub)
Outputs:
- freshness statuses
- compliance snapshot aggregates
"""

import csv, json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional

CADENCE_WINDOWS = {
    "hourly": timedelta(hours=1),
    "daily": timedelta(days=1),
    "weekly": timedelta(days=7),
    "monthly": timedelta(days=30),
    "quarterly": timedelta(days=91),
    "yearly": timedelta(days=365),
}

def parse_cadence(cadence: str) -> timedelta:
    if cadence.startswith("custom:"):
        hours = int(cadence.split(":",1)[1])
        return timedelta(hours=hours)
    return CADENCE_WINDOWS.get(cadence, timedelta(days=30))

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def load_requirements_csv(path: str) -> List[Dict[str, Any]]:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        out = []
        for r in reader:
            r["required"] = (r["required"].lower() == "true")
            try:
                r["scope_tags"] = json.loads(r["scope_tags_json"] or "{}")
            except Exception:
                r["scope_tags"] = {}
            out.append(r)
        return out

# ---- Registry client (stub) ----
def registry_find_latest(evidence_id: str, environment: str, scope_tags: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Return latest evidence item matching evidence_id+env+tags.
    Replace with real query to Evidence Registry.
    """
    return None

def evaluate_requirement(req: Dict[str, Any], environment: str) -> Dict[str, Any]:
    item = registry_find_latest(req["evidence_id"], environment, req.get("scope_tags",{}))
    computed_at = now_utc().isoformat()
    cadence_td = parse_cadence(req["cadence"])
    status = "missing"
    last_collected_at = None
    age_seconds = None
    expires_at = None
    artifact_uri = None
    artifact_sha256 = None
    registry_event_id = None

    if item:
        last_collected_at = item.get("collected_at")
        expires_at = item.get("expires_at")
        artifact_uri = item.get("artifact_uri")
        artifact_sha256 = item.get("artifact_sha256")
        registry_event_id = item.get("registry_event_id")

        try:
            t = datetime.fromisoformat(last_collected_at.replace("Z","+00:00"))
            age = now_utc() - t
            age_seconds = int(age.total_seconds())
            if expires_at and now_utc() > datetime.fromisoformat(expires_at.replace("Z","+00:00")):
                status = "expired"
            elif age <= cadence_td:
                status = "fresh"
            else:
                status = "stale"
        except Exception:
            status = "unknown"

    return {
        "environment": environment,
        "policy_pack": req["policy_pack"],
        "control": req["control"],
        "evidence_id": req["evidence_id"],
        "scope_tags": req.get("scope_tags",{}),
        "status": status,
        "cadence": req["cadence"],
        "last_collected_at": last_collected_at,
        "age_seconds": age_seconds,
        "expires_at": expires_at,
        "artifact_sha256": artifact_sha256,
        "artifact_uri": artifact_uri,
        "registry_event_id": registry_event_id,
        "verification": {"hash_ok": None, "signature_ok": None, "attestation_ok": None},
        "computed_at": computed_at,
        "details": {"required": req.get("required", True)}
    }

def compute_snapshot(requirements: List[Dict[str,Any]], environment: str, policy_packs: Optional[List[str]]=None) -> Dict[str, Any]:
    if policy_packs:
        requirements = [r for r in requirements if r["policy_pack"] in policy_packs]

    statuses = [evaluate_requirement(r, environment) for r in requirements if r.get("required", True)]

    counts = {"fresh":0,"stale":0,"missing":0,"expired":0,"unknown":0}
    for s in statuses:
        counts[s["status"]] = counts.get(s["status"],0) + 1

    total = sum(counts.values()) or 1
    coverage = (counts["fresh"] / total) * 100.0

    return {
        "snapshot_id": f"SNAP-{int(now_utc().timestamp())}",
        "environment": environment,
        "policy_packs": sorted(list(set([s["policy_pack"] for s in statuses]))),
        "computed_at": now_utc().isoformat(),
        "coverage_percent": round(coverage, 2),
        "counts": counts,
        "top_missing": [s for s in statuses if s["status"]=="missing"][:10],
        "top_stale": [s for s in statuses if s["status"]=="stale"][:10],
        "by_control": [],
        "by_domain": []
    }

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--requirements", required=True)
    p.add_argument("--environment", required=True)
    args = p.parse_args()
    reqs = load_requirements_csv(args.requirements)
    snap = compute_snapshot(reqs, args.environment)
    print(json.dumps(snap, ensure_ascii=False, indent=2))
