# IFOS CLI Stub v1
# Example:
#   python IFOS_cli_stub_v1.py install plan.json
#   python IFOS_cli_stub_v1.py run job.json

import json
import sys

def load(path):
    with open(path,"r",encoding="utf-8") as f:
        return json.load(f)

def main(argv):
    if len(argv) < 3:
        print("Usage: python IFOS_cli_stub_v1.py (install|run|rollback) <file.json>")
        return 2
    cmd, path = argv[1], argv[2]
    obj = load(path)
    print(f"[IFOS CLI] cmd={cmd} id={obj.get('plan_id') or obj.get('job_id') or obj.get('rollback_id')} target={obj.get('target')}")
    # Stub: call Execution API here
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
