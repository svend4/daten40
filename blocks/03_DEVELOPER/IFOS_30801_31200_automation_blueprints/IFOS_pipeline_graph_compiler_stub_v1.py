# IFOS Pipeline Graph Compiler Stub v1
from __future__ import annotations
from typing import Dict, Any

def compile_to_ifos_job(graph: Dict[str, Any]) -> Dict[str, Any]:
    return {"job_kind":"ifos_native","graph":graph}
