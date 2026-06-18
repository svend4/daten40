# ifos_mock_server_stub_v1.py
from __future__ import annotations
from typing import Dict

def create_mock(source: Dict) -> Dict:
    return {"mock_id":"mock.generated","routes":[],"modes":["ok","errors"],"version":"1.0.0"}
