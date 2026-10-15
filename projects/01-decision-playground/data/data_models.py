from dataclasses import dataclass
from .models import StepOutcome


@dataclass
class StepOutput:
    position: tuple[int, int]
    outcome: StepOutcome
