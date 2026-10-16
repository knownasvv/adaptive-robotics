from dataclasses import dataclass
from .models import NavigationState, StepOutcome, StoppingReason


@dataclass
class StepOutput:
    position: tuple[int, int]
    outcome: StepOutcome

@dataclass
class PathExecutionOutput:
    position: tuple[int, int]
    executed_count: int
    stopping_reason: StoppingReason

@dataclass
class NavigationOutput:
    execution: PathExecutionOutput
    state_history: list[NavigationState]