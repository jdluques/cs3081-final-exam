from dataclasses import dataclass


@dataclass(frozen=True)
class AttendancePolicy:
    minimum_required: bool = True

    def is_eligible(self, has_reached_minimum: bool) -> bool:
        return has_reached_minimum
