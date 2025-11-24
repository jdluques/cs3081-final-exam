from dataclasses import dataclass
from typing import List

from app.domain.entities.evaluation import Evaluation


@dataclass
class Student:
    student_id: int
    evaluations: List[Evaluation]
    has_reached_minimun_classes: bool
