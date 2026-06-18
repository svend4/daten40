# ifos_course_builder_stub_v1.py
from __future__ import annotations
from typing import Dict, List

def build_course(course_id: str, title: str, level: str, lessons: List[str], labs: List[str]) -> Dict:
    return {"course_id":course_id,"title":title,"level":level,"lessons":lessons,"labs":labs,"version":"1.0.0"}
