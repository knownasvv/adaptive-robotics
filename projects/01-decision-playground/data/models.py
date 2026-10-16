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
    GOAL_REACHED = 'robot reaches the goal'
    STEP_LIMIT = 'action budget expires before completion'
    EXECUTION_FAILED = 'attempted movement fails'


class NavigationState(Enum):
    IDLE = 'no navigation attempt is active',
    PLANNING = 'finding a route to the requested goal',
    EXECUTING = 'following the route',
    SUCCEEDED = 'the robot reached the goal',
    FAILED = 'the navigation attempt ended unsuccessfully'


class NavigationEvent(Enum):
    START = 1
    PATH_FOUND = 2
    ALREADY_AT_GOAL = 3
    NO_PATH = 4
    GOAL_REACHED = 5
    MOVEMENT_FAILED = 6
    BUDGET_EXHAUSTED = 7