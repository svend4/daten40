
from .utils import write_json, now_z
from .base import CollectorError
import os

PLUGIN_NAME="audit_log_exporter"
PLUGIN_VERSION="1.0.0"

def collect(job: dict, config: dict) -> dict:
    # TODO: integrate real audit log source via connector
    evidence_id = job["evidence_id"]
    fmt = job.get("format","json")
    out = f"/tmp/{PLUGIN_NAME}_{evidence_id}_{now_z().replace(':','')}.{fmt}"
    payload = {
        "evidence_id": evidence_id,
        "exported_at": now_z(),
        "time_window": job.get("time_window"),
        "records": [
            {"event":"access", "subject":"CUST-100", "resource":"phi_record", "ts": now_z()}
        ]
    }
    if fmt in ("json","ndjson"):
        write_json(out, payload)
    elif fmt == "csv":
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out,"w",encoding="utf-8") as f:
            f.write("event,subject,resource,ts\n")
            for r in payload["records"]:
                f.write(f"{r['event']},{r['subject']},{r['resource']},{r['ts']}\n")
    else:
        raise CollectorError("DATA_FORMAT", f"Unsupported format: {fmt}", retryable=False)

    return {
        "artifact_path": out,
        "artifact_format": fmt,
        "metadata": {
            "collector": f"{PLUGIN_NAME}@{PLUGIN_VERSION}",
            "source_system": "audit_log",
            "source_version": "stub",
            "region": config.get("region","unknown"),
            "tags": job.get("tags",{})
        }
    }
