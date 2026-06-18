
"""Webhook-to-Queue Enqueue skeleton.
Policy engine can call this to request evidence on demand.
"""
from fastapi import FastAPI
app = FastAPI(title="IFOS Evidence Enqueue")

@app.post("/enqueue")
def enqueue(payload: dict):
    # TODO: validate, add idempotency_key, push to queue
    return {"queued": True, "job_id": payload.get("job_id")}
