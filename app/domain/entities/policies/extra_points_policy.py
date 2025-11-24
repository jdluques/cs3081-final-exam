from dataclasses import dataclass


@dataclass(frozen=True)
class ExtraPointsPolicy:
    all_years_teachers_agree: bool
    bonus_if_agree: float = 0.5
    max_final_grade: float = 20.0


def compute_bonus(
    self, base_grade: float, evaluations_count: int, has_reached_minimum: bool
) -> float:
    if not self.all_years_teachers_agree:
        return 0.0
    if not has_reached_minimum:
        return 0.0
    if evaluations_count <= 0:
        return 0.0
    potential = base_grade + self.bonus_if_agree
    if potential > self.max_final_grade:
        return max(0.0, self.max_final_grade - base_grade)
    return self.bonus_if_agree
