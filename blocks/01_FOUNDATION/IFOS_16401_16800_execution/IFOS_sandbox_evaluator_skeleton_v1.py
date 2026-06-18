# IFOS Sandbox Evaluator Skeleton v1
from __future__ import annotations
from typing import Dict, Any, List
import re

class Sandbox:
    def __init__(self, policy: Dict[str, Any]):
        self.policy = policy

    def precheck(self, job: Dict[str, Any]) -> None:
        # Stub: enforce flags_policy thresholds
        # Example: if money flag and require_signed, deny unless build signed.
        flags = job.get("labels", {}).get("flags", {})
        fp = self.policy.get("flags_policy", {})
        if flags.get("money") and fp.get("money", {}).get("require_signed", False):
            raise PermissionError("Policy requires signed artifacts for money=true jobs.")

    def redact(self, text: str, resolved_secrets: Dict[str, str]) -> str:
        # Replace secret values
        out = text or ""
        if self.policy.get("redaction", {}).get("mask_secrets", True):
            for _, val in (resolved_secrets or {}).items():
                if not val: 
                    continue
                out = out.replace(val, "***REDACTED***")
        # Pattern-based redaction
        for pat in self.policy.get("redaction", {}).get("patterns", []) or []:
            try:
                out = re.sub(pat, "***REDACTED***", out)
            except re.error:
                pass
        return out
