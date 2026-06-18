# ifos_quiz_engine_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def grade(answers: List[int], correct: List[int]) -> Dict:
    score = sum(1 for a,c in zip(answers, correct) if a==c)
    return {"score":score,"total":len(correct),"passed": score>=int(0.7*len(correct))}
