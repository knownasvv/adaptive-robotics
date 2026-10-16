from enum import Enum


class StepAction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    WAIT = 5


class StepOutcome(Enum):
    MOVED = 1
    BLOCKED = 2
    OUT_OF_BOUNDS = 3
    WAITED = 4
 
 
class StoppingReason(Enum):
    NO_PATH = 0
    GOAL_REACHED = 1 # robot reaches the goal
    STEP_LIMIT = 2 # action budget expires before completion
    EXECUTION_FAILED = 3 # attempted movement fails