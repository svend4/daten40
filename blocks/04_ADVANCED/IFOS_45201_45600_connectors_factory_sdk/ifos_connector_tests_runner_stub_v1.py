# ifos_connector_tests_runner_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def run_tests(connector: Dict, suite: Dict) -> List[Dict]:
    results=[]
    for t in suite.get("tests", []):
        results.append({"test":t.get("name"),"ok":True})
    return results
