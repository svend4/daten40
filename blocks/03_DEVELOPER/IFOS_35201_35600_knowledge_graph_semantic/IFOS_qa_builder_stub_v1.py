# IFOS QA Builder Stub v1
from __future__ import annotations
from typing import Dict, Any, List

def build(question: str, bundles: List[str]) -> Dict[str, Any]:
    return {
        "question": question,
        "short_answer": "См. рекомендуемые bundles и шаги настройки.",
        "recommended": bundles,
        "setup_steps": ["Выбрать bundle", "Подключить коннекторы", "Запустить dry-run", "Включить прод режим"]
    }
