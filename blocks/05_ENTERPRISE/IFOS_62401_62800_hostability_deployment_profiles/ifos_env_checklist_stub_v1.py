# ifos_env_checklist_stub_v1.py
from __future__ import annotations
import os

REQUIRED = ["PORT"]
SUGGESTED = ["API_BASE_URL","FRONTEND_ORIGIN","DATABASE_URL","REDIS_URL"]

def main():
    missing = [k for k in REQUIRED if not os.getenv(k)]
    print("required_missing:", missing)
    for k in SUGGESTED:
        print(k, "=", "set" if os.getenv(k) else "unset")

if __name__ == "__main__":
    main()
