# ifos_secret_runtime_injector_stub_v1.py
from __future__ import annotations
from typing import Dict

def inject(run_env: Dict, secret_token: Dict) -> Dict:
    # placeholder: returns redacted env vars
    return {"ENV": run_env.get("env","dev"), "SECRET_TOKEN": "***"}
