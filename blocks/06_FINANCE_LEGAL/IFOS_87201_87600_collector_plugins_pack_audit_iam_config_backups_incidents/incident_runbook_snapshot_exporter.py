
from .utils import now_z
from .base import CollectorError
import os, zipfile, tempfile, pathlib

PLUGIN_NAME="incident_runbook_snapshot_exporter"
PLUGIN_VERSION="1.0.0"

def collect(job: dict, config: dict) -> dict:
    fmt = job.get("format","zip")
    ts = now_z().replace(":","")
    if fmt == "md":
        out = f"/tmp/{PLUGIN_NAME}_{job['evidence_id']}_{ts}.md"
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out,"w",encoding="utf-8") as f:
            f.write("# Incident Response Runbook (Snapshot)\n\n- Detect\n- Triage\n- Contain\n- Eradicate\n- Recover\n")
    elif fmt == "zip":
        out = f"/tmp/{PLUGIN_NAME}_{job['evidence_id']}_{ts}.zip"
        with tempfile.TemporaryDirectory() as td:
            td = pathlib.Path(td)
            (td/"runbook.md").write_text("# Incident Runbook\n\nSteps...", encoding="utf-8")
            (td/"postmortem_template.md").write_text("# Postmortem\n\nTimeline...", encoding="utf-8")
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
            "source_system": "docs/itsm",
            "source_version": "stub",
            "region": config.get("region","unknown"),
            "tags": job.get("tags",{})
        }
    }
