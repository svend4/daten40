# ifos_mock_server_fastapi_stub_v1.py
from __future__ import annotations
from fastapi import FastAPI, Request
from typing import Dict, Any
import random, time

app = FastAPI(title="IFOS Mock Server")

STATE: Dict[str, Any] = {"orders": []}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/v1/products")
def list_products():
    # Minimal deterministic placeholder
    return {"items": [{"id": "p1", "price": 9.99}, {"id": "p2", "price": 14.50}]}

@app.post("/v1/orders")
async def create_order(req: Request):
    body = await req.json()
    oid = f"o{len(STATE['orders'])+1}"
    STATE["orders"].append({"id": oid, "body": body, "status": "created"})
    # Simulate latency
    time.sleep(0.12)
    return {"id": oid, "status": "created"}
