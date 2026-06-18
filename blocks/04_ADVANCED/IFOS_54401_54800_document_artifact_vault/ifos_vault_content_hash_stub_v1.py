# ifos_vault_content_hash_stub_v1.py
import hashlib
def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()
