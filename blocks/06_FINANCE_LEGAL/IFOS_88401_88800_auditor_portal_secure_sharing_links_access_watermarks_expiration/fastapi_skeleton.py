
"""Auditor Portal + Secure Sharing — FastAPI skeleton.

Implements:
- share link create/revoke/list (admin)
- portal session start (auditor)
- artifact listing + download issuance
- simple download counters

TODO:
- email verification / MFA
- IP allowlists
- rate limiting
- signed URLs from object storage
- watermarking pipeline integration
- append-only download/access event sink (WORM)
"""
from fastapi import FastAPI, HTTPException, Header
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
import uuid, hashlib, secrets

app = FastAPI(title="IFOS Auditor Portal", version="1.0.0")

SHARES: Dict[str, Dict[str, Any]] = {}
SESSIONS: Dict[str, Dict[str, Any]] = {}
DOWNLOAD_COUNTS: Dict[str, int] = {}

def now():
    return datetime.now(timezone.utc)

def token_hash(tok: str) -> str:
    return hashlib.sha256(tok.encode("utf-8")).hexdigest()

@app.post("/sharelinks/create")
def sharelinks_create(payload: Dict[str, Any]) -> Dict[str, Any]:
    share_id = f"SHR-{uuid.uuid4()}"
    tok = secrets.token_urlsafe(32)
    expires_at = now() + timedelta(seconds=int(payload.get("ttl_seconds", 7*24*3600)))

    rec = {
        "share_id": share_id,
        "report_id": payload["report_id"],
        "auditor_email": payload.get("auditor_email"),
        "created_at": now().isoformat(),
        "expires_at": expires_at.isoformat(),
        "status": "active",
        "allowed_files": payload.get("allowed_files", ["report.pdf", "audit_pack.zip"]),
        "ip_allowlist": payload.get("ip_allowlist"),
        "max_downloads": payload.get("max_downloads"),
        "require_email_verification": bool(payload.get("require_email_verification", False)),
        "watermark_enabled": bool(payload.get("watermark_enabled", True)),
        "token_hash": token_hash(tok),
        "notes": payload.get("notes")
    }
    SHARES[share_id] = rec
    DOWNLOAD_COUNTS[share_id] = 0

    share_url = f"https://portal.example.com/s/{share_id}?token={tok}"
    return {"share_id": share_id, "share_url": share_url, "expires_at": rec["expires_at"], "status": "active"}

@app.post("/sharelinks/revoke")
def sharelinks_revoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    share_id = payload["share_id"]
    rec = SHARES.get(share_id)
    if not rec:
        raise HTTPException(404, "share not found")
    rec["status"] = "revoked"
    rec["revoked_at"] = now().isoformat()
    rec["revoke_reason"] = payload.get("reason")
    return {"share_id": share_id, "status": "revoked"}

@app.post("/sharelinks/list")
def sharelinks_list(payload: Dict[str, Any]) -> Dict[str, Any]:
    report_id = payload.get("report_id")
    status = payload.get("status")
    items = list(SHARES.values())
    if report_id:
        items = [x for x in items if x.get("report_id") == report_id]
    if status:
        items = [x for x in items if x.get("status") == status]
    limit = int(payload.get("limit", 50))
    return {"items": items[:limit]}

@app.post("/portal/session/start")
def portal_session_start(payload: Dict[str, Any], user_agent: Optional[str] = Header(default=None)) -> Dict[str, Any]:
    tok = payload.get("share_token")
    if not tok:
        raise HTTPException(400, "share_token required")

    th = token_hash(tok)
    rec = next((x for x in SHARES.values() if x.get("token_hash") == th), None)
    if not rec:
        raise HTTPException(403, "invalid token")

    if rec["status"] != "active":
        raise HTTPException(403, f"share is {rec['status']}")

    # Simple expiry check
    exp = datetime.fromisoformat(rec["expires_at"].replace("Z", "+00:00"))
    if now() > exp:
        rec["status"] = "expired"
        raise HTTPException(403, "share expired")

    session_id = f"SES-{uuid.uuid4()}"
    SESSIONS[session_id] = {
        "session_id": session_id,
        "share_id": rec["share_id"],
        "report_id": rec["report_id"],
        "auditor_email": rec.get("auditor_email"),
        "expires_at": rec["expires_at"],
        "allowed_files": rec.get("allowed_files", []),
        "watermark_enabled": rec.get("watermark_enabled", True),
        "user_agent": user_agent
    }
    return SESSIONS[session_id]

@app.get("/portal/artifacts/list")
def portal_artifacts_list(session_id: str) -> Dict[str, Any]:
    ses = SESSIONS.get(session_id)
    if not ses:
        raise HTTPException(403, "invalid session")
    items = []
    for f in ses.get("allowed_files", []):
        kind = "table" if f.startswith("tables/") else ("report" if f.endswith(".pdf") else "audit_pack")
        items.append({"artifact_id": f, "name": f, "sha256": None, "bytes": None, "kind": kind})
    return {"items": items}

@app.post("/portal/download")
def portal_download(payload: Dict[str, Any]) -> Dict[str, Any]:
    ses = SESSIONS.get(payload.get("session_id"))
    if not ses:
        raise HTTPException(403, "invalid session")
    artifact_id = payload.get("artifact_id")
    if artifact_id not in ses.get("allowed_files", []):
        raise HTTPException(403, "artifact not allowed")

    share_id = ses["share_id"]
    max_dl = SHARES.get(share_id, {}).get("max_downloads")
    if max_dl is not None and DOWNLOAD_COUNTS.get(share_id, 0) >= int(max_dl):
        raise HTTPException(429, "download limit exceeded")

    DOWNLOAD_COUNTS[share_id] = DOWNLOAD_COUNTS.get(share_id, 0) + 1
    expires = now() + timedelta(minutes=10)

    # Placeholder for object-store signed URL
    return {
        "download_url": f"https://storage.example.com/download/{ses['report_id']}/{artifact_id}",
        "expires_at": expires.isoformat()
    }
