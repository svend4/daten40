# ifos_dns_check_stub_v1.py
from __future__ import annotations
import socket
def resolve(host: str):
    try:
        return socket.gethostbyname_ex(host)
    except Exception as e:
        return {"error": str(e)}
if __name__ == "__main__":
    for h in ["api.example.com","app.example.com"]:
        print(h, resolve(h))
