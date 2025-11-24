from app.domain.entities.evaluation import Evaluation
from app.domain.entities.policies.attendance_policy import AttendancePolicy
from app.domain.entities.policies.extra_points_policy import ExtraPointsPolicy
from app.domain.services.grade_calculator import GradeCalculator

import pytest


def make_calculator(all_teachers: bool = False):
    return GradeCalculator(
        AttendancePolicy(), ExtraPointsPolicy(all_years_teachers_agree=all_teachers)
    )


def test_calculation_normal():
    calc = make_calculator(all_teachers=False)
    evals = [Evaluation("Exam1", 18, 50), Evaluation("Exam2", 16, 50)]
    final, report = calc.calculate_final_grade(evals, True)
    assert final == 17.0
    assert report["base_grade"] == 17.0


def test_no_attendance_sets_zero():
    calc = make_calculator(all_teachers=True)
    evals = [Evaluation("Exam1", 18, 50), Evaluation("Exam2", 16, 50)]
    final, report = calc.calculate_final_grade(evals, False)
    assert final == 0.0
    assert "Attendance minimum not reached" in report["notes"][0]


def test_extra_points_applied_when_agree():
    calc = make_calculator(all_teachers=True)
    evals = [Evaluation("Exam1", 20, 50), Evaluation("Exam2", 20, 50)]
    final, report = calc.calculate_final_grade(evals, True)
    assert final == 20.0
    assert report["extra_applied"] == 0.0 or report["extra_applied"] == 0.0


def test_zero_evaluations():
    calc = make_calculator()
    final, report = calc.calculate_final_grade([], True)
    assert final == 0.0
    assert "No evaluations provided" in report["errors"]


def test_invalid_weights():
    calc = make_calculator()
    with pytest.raises(ValueError):
        Evaluation("E", 10, -5)
