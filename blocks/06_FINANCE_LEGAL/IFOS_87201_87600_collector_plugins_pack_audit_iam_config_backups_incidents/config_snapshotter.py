
from .utils import write_json, now_z
from .base import CollectorError
import os, zipfile, tempfile, pathlib

PLUGIN_NAME="config_snapshotter"
PLUGIN_VERSION="1.0.0"

def collect(job: dict, config: dict) -> dict:
    fmt = job.get("format","zip")
    ts = now_z().replace(":","")
    if fmt == "json":
        out = f"/tmp/{PLUGIN_NAME}_{job['evidence_id']}_{ts}.json"
        write_json(out, {
            "evidence_id": job["evidence_id"],
            "snapshotted_at": now_z(),
            "rbac": {"policies": ["admin:all", "support:read"]},
            "network": {"tls": "enforced"}
        })
    elif fmt == "zip":
        out = f"/tmp/{PLUGIN_NAME}_{job['evidence_id']}_{ts}.zip"
        with tempfile.TemporaryDirectory() as td:
            td = pathlib.Path(td)
            (td/"rbac.json").write_text('{"policies":["admin:all","support:read"]}', encoding="utf-8")
            (td/"security_baseline.json").write_text('{"tls":"enforced","mfa":"required"}', encoding="utf-8")
            with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
                for p in td.rglob("*"):
                    z.write(p, arcname=p.name)
    else:
        raise CollectorError("DATA_FORMAT", f"Unsupported format: {fmt}", retryable=False)

    return {
        "artifact_path": out,
        "artifact_format": fmt,
        "metadata": {
            "collector": f"{PLUGIN_NAME}@{PLUGIN_VERSION}",
            "source_system": "config_store",
            "source_version": "stub",
            "region": config.get("region","unknown"),
            "tags": job.get("tags",{})
        }
    }
