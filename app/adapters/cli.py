import json

from app.application.use_cases.calculate_grade import CalculateGradeUseCase
from app.domain.entities.evaluation import Evaluation
from app.domain.entities.policies.attendance_policy import AttendancePolicy
from app.domain.entities.policies.extra_points_policy import ExtraPointsPolicy
from app.domain.services.grade_calculator import GradeCalculator


def parse_evaluations_from_input():
    print("Enter evaluations one per line as: name,grade,weight (empty line to finish)")
    evals = []
    while True:
        line = input().strip()
        if not line:
            break
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 3:
            print("Invalid format, expected 3 comma-separated values")
            continue
        name, grade_s, weight_s = parts
        try:
            grade = float(grade_s)
            weight = float(weight_s)
            evals.append(Evaluation(name=name, grade=grade, weight=weight))
        except Exception as e:
            print(f"Error parsing evaluation: {e}")
    return evals


def run_cli():
    print("CS-GradeCalculator CLI")
    student_id = input("Student identifier: ")
    evaluations = parse_evaluations_from_input()
    att = input("Did the student reach minimum attendance? (y/n): ")
    has_att = att.lower().startswith("y")
    all_teachers = input("Do all years' teachers agree on extra points? (y/n): ")
    extra_policy = ExtraPointsPolicy(
        all_years_teachers_agree=all_teachers.lower().startswith("y")
    )
    attendance_policy = AttendancePolicy()
    calculator = GradeCalculator(attendance_policy, extra_policy)
    use_case = CalculateGradeUseCase(calculator)
    final, report = use_case.execute(evaluations, has_att)
    print("--- Report ---")
    print(json.dumps(report, indent=2))
    print(f"Final grade for {student_id}: {final}")


if __name__ == "__main__":
    run_cli()
