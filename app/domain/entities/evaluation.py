from dataclasses import dataclass


@dataclass(frozen=True)
class Evaluation:
    name: str
    weight: float
    grade: float

    def __post_init__(self):
        if not (0 <= self.grade <= 20):
            raise ValueError("score must be between 0 and 20")
        if not (0 <= self.weight <= 100):
            raise ValueError("weight must be between 0 and 100")
