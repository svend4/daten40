
from .utils import write_json, now_z
from .base import CollectorError
import os

PLUGIN_NAME="backup_restore_test_collector"
PLUGIN_VERSION="1.0.0"

def collect(job: dict, config: dict) -> dict:
    fmt = job.get("format","json")
    out = f"/tmp/{PLUGIN_NAME}_{job['evidence_id']}_{now_z().replace(':','')}.{fmt}"
    report = {
        "evidence_id": job["evidence_id"],
        "tested_at": now_z(),
        "result": "pass",
        "rto_minutes": 30,
        "rpo_minutes": 15,
        "notes": "Stub report"
    }
    if fmt == "json":
        write_json(out, report)
    elif fmt == "csv":
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out,"w",encoding="utf-8") as f:
            f.write("tested_at,result,rto_minutes,rpo_minutes,notes\n")
            f.write(f"{report['tested_at']},{report['result']},{report['rto_minutes']},{report['rpo_minutes']},{report['notes']}\n")
    else:
        raise CollectorError("DATA_FORMAT", f"Unsupported format: {fmt}", retryable=False)

    return {
        "artifact_path": out,
        "artifact_format": fmt,
        "metadata": {
            "collector": f"{PLUGIN_NAME}@{PLUGIN_VERSION}",
            "source_system": "backup_system",
            "source_version": "stub",
            "region": config.get("region","unknown"),
            "tags": job.get("tags",{})
        }
    }
