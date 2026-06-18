# ifos_egress_check_stub_v1.py
from __future__ import annotations
import urllib.request, sys
def check(url: str):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.status
    except Exception as e:
        return f"error:{e}"
if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv)>1 else "https://example.com"
    print(url, check(url))
