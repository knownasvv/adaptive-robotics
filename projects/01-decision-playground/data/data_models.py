from dataclasses import dataclass
from .models import StepOutcome


@dataclass
class Point:
    x: int
    y: int


@dataclass
class StepOutput:
    position: Point
    outcome: StepOutcome