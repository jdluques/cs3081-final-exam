from typing import Iterable

from app.domain.entities.evaluation import Evaluation
from app.domain.services.grade_calculator import GradeCalculator


class CalculateGradeUseCase:
    def __init__(self, grade_calculator: GradeCalculator):
        self.grade_calculator = grade_calculator

    def execute(
        self, evaluations: Iterable[Evaluation], has_reached_minimum_classes: bool
    ):
        return self.grade_calculator.calculate_final_grade(
            evaluations, has_reached_minimum_classes
        )
