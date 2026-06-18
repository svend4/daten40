# IFOS Adapter Examples (stubs) v1
# Demonstrates how adapters implement validate/execute/redact.

from __future__ import annotations
from typing import Dict, Any, List

class AdapterContext:
    def __init__(self, mode: str, sandbox, secrets: Dict[str,str], state, job_id: str, trace_id: str):
        self.mode = mode
        self.sandbox = sandbox
        self.secrets = secrets
        self.state = state
        self.job_id = job_id
        self.trace_id = trace_id

class Adapter:
    def validate(self, params: Dict[str, Any]) -> List[str]: return []
    def execute(self, params: Dict[str, Any], ctx: AdapterContext) -> Dict[str, Any]: raise NotImplementedError
    def redact(self, obj: Any) -> Any: return obj

class TelegramSendMessageAdapter(Adapter):
    def validate(self, params: Dict[str, Any]) -> List[str]:
        errs = []
        if not params.get("chat_id"): errs.append("chat_id is required")
        if not params.get("text"): errs.append("text is required")
        # token comes from ctx.secrets
        return errs

    def execute(self, params: Dict[str, Any], ctx: AdapterContext) -> Dict[str, Any]:
        # DRY-RUN: do not send
        if ctx.mode == "dry_run":
            return {"ok": True, "dry_run": True, "preview_len": len(params.get("text",""))}

        token = ctx.secrets.get("TELEGRAM_BOT_TOKEN","")
        if not token or token.startswith("REDACTED"):
            raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in ctx.secrets")

        # Sandbox guard example: prevent sending if host not allowed (conceptual)
        if ctx.sandbox and ("api.telegram.org" not in getattr(ctx.sandbox, "allow_hosts", set())):
            raise RuntimeError("Sandbox: api.telegram.org not in allowlist")

        # Real HTTP call omitted in stub
        return {"ok": True, "message_id": 123}

    def redact(self, obj: Any) -> Any:
        # remove token if ever appears
        if isinstance(obj, dict):
            out = dict(obj)
            if "token" in out: out["token"] = "***"
            if "text" in out and isinstance(out["text"], str) and len(out["text"]) > 200:
                out["text"] = out["text"][:200] + "…"
            return out
        return obj

class RssReadFeedAdapter(Adapter):
    def validate(self, params: Dict[str, Any]) -> List[str]:
        errs = []
        if not params.get("url"): errs.append("url is required")
        return errs

    def execute(self, params: Dict[str, Any], ctx: AdapterContext) -> Dict[str, Any]:
        url = params["url"]
        if ctx.mode == "dry_run":
            return {"items": [], "dry_run": True}
        if ctx.sandbox and (url.split("/")[2] not in getattr(ctx.sandbox, "allow_hosts", set())):
            raise RuntimeError("Sandbox: RSS host not in allowlist")
        # Real RSS fetch omitted in stub
        return {"items":[{"guid":"a1","title":"Hello","link":"https://example.com/a1"}]}
