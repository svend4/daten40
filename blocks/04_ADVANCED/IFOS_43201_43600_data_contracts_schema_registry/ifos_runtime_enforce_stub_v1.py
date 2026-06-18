# ifos_runtime_enforce_stub_v1.py
from __future__ import annotations
from typing import Dict, Any

def enforce(payload: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
    # stub: if policy says coerce numbers, convert numeric strings
    actions=policy.get("actions", [])
    do_coerce=any(a.get("do")=="coerce" for a in actions)
    if do_coerce:
        for k,v in list(payload.items()):
            if isinstance(v, str) and v.replace(".","",1).isdigit():
                # naive numeric coercion
                payload[k]=float(v) if "." in v else int(v)
    return payload
