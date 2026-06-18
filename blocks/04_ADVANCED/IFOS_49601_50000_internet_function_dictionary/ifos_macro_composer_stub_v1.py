# ifos_macro_composer_stub_v1.py
from __future__ import annotations
from typing import Dict

def compose(terms):
    return {"macro":{"steps":terms,"gates":["preflight"],"exports":["docker_compose"]}}
