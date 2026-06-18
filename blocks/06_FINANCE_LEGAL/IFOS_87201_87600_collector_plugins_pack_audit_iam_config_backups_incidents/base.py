
"""Collector Plugin Interface (reference).

Each plugin must expose:
- PLUGIN_NAME, PLUGIN_VERSION
- collect(job: dict, config: dict) -> dict
  returns:
    - artifact_path (local file)
    - artifact_format
    - metadata (collector/source/provenance/tags)
"""

from typing import Dict, Any

class CollectorError(Exception):
    def __init__(self, code: str, message: str, retryable: bool):
        super().__init__(message)
        self.code = code
        self.retryable = retryable

def collect(job: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    raise NotImplementedError("Plugin must implement collect()")
