
from .utils import write_json, now_z
from .base import CollectorError
import os

PLUGIN_NAME="iam_exporter"
PLUGIN_VERSION="1.0.0"

def collect(job: dict, config: dict) -> dict:
    fmt = job.get("format","csv")
    out = f"/tmp/{PLUGIN_NAME}_{job['evidence_id']}_{now_z().replace(':','')}.{fmt}"
    records = [
        {"user":"alice", "role":"admin", "mfa":"enabled", "reviewed_at": now_z()},
        {"user":"bob", "role":"support", "mfa":"enabled", "reviewed_at": now_z()},
    ]
    if fmt == "json":
        write_json(out, {"evidence_id": job["evidence_id"], "exported_at": now_z(), "records": records})
    elif fmt == "csv":
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out,"w",encoding="utf-8") as f:
            f.write("user,role,mfa,reviewed_at\n")
            for r in records:
                f.write(f"{r['user']},{r['role']},{r['mfa']},{r['reviewed_at']}\n")
    else:
        raise CollectorError("DATA_FORMAT", f"Unsupported format: {fmt}", retryable=False)

    return {
        "artifact_path": out,
        "artifact_format": fmt,
        "metadata": {
            "collector": f"{PLUGIN_NAME}@{PLUGIN_VERSION}",
            "source_system": "iam",
            "source_version": "stub",
            "region": config.get("region","unknown"),
            "tags": job.get("tags",{})
        }
    }
