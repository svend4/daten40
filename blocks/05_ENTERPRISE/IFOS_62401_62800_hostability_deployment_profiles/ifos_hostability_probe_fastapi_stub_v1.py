# ifos_hostability_probe_fastapi_stub_v1.py
from __future__ import annotations
from fastapi import FastAPI
import os, socket, time

app = FastAPI(title="IFOS Hostability Probe")

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/probe/env")
def probe_env():
    # minimal signals: port env, hostname, time
    return {
        "PORT": os.getenv("PORT"),
        "HOSTNAME": socket.gethostname(),
        "UTC": time.time(),
        "BIND_HINT": "0.0.0.0"
    }

@app.get("/probe/features")
def probe_features():
    # placeholder; real probe would test ws/streaming/storage/write etc.
    return {"detected": ["INBOUND_HTTP", "OUTBOUND_EGRESS"], "missing": []}
