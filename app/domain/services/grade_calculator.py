from typing import Iterable, List, Tuple

from app.domain.entities.evaluation import Evaluation
from app.domain.entities.policies.attendance_policy import AttendancePolicy
from app.domain.entities.policies.extra_points_policy import ExtraPointsPolicy

MAX_FINAL_GRADE = 20.0


class GradeCalculator:
    def __init__(
        self, attendance_policy: AttendancePolicy, extra_policy: ExtraPointsPolicy
    ):
        self.attendance_policy = attendance_policy
        self.extra_policy = extra_policy

    def validate_evaluations(
        self, evaluations: Iterable[Evaluation]
    ) -> Tuple[List[Evaluation], List[str]]:
        evals = list(evaluations)
        errors = []
        total_weight = sum(e.weight for e in evals)
        if len(evals) == 0:
            errors.append("No evaluations provided")
        if any(e.weight < 0 or e.weight > 100 for e in evals):
            errors.append("One or more evaluations have invalid weight")
        if total_weight <= 0:
            errors.append("Total weight must be positive")
        return evals, errors

    def calculate_base_grade(self, evaluations: Iterable[Evaluation]) -> float:
        evals = list(evaluations)
        total_weight = sum(e.weight for e in evals)
        if total_weight <= 0:
            return 0.0
        weighted_sum = sum((e.grade * e.weight) for e in evals)
        base = weighted_sum / total_weight
        return round(base, 2)

    def calculate_final_grade(
        self, evaluations: Iterable[Evaluation], has_reached_minimum_classes: bool
    ) -> Tuple[float, dict]:
        evals, errors = self.validate_evaluations(evaluations)
        report = {
            "evaluations": [e.__dict__ for e in evals],
            "errors": errors,
            "extra_applied": 0.0,
            "notes": [],
        }
        base = self.calculate_base_grade(evals)
        report["base_grade"] = base

        if not self.attendance_policy.is_eligible(has_reached_minimum_classes):
            report["notes"].append(
                "Attendance minimum not reached — final grade set to 0"
            )
            final = 0.0
            report["final_grade"] = final
            return final, report

        bonus = self.extra_policy.compute_bonus(
            base, len(evals), has_reached_minimum_classes
        )
        report["extra_applied"] = round(bonus, 2)

        final = base + bonus
        if final > MAX_FINAL_GRADE:
            report["notes"].append("Final grade capped to maximum allowed")
            final = MAX_FINAL_GRADE

        final = round(final, 2)
        report["final_grade"] = final
        return final, report
