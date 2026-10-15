# Execute the selected route and inspect actual outcomes

import copy

from data.data_models import Point, StepOutput
from data.models import StepAction, StepOutcome

def _get_outcome(grid: Point, obstacles: list[Point], position: Point, action: StepAction) -> StepOutcome:
    if action == StepAction.WAIT:
        return StepOutcome.WAITED

    if position.x >= grid.x or position.y >= grid.y or position.x < 0 or position.y < 0:
        return StepOutcome.OUT_OF_BOUNDS

    for obstacle in obstacles:
        if position == obstacle:
            return StepOutcome.BLOCKED

    return StepOutcome.MOVED


def step(
    grid: Point,
    obstacles: list[Point], 
    current_position: Point, 
    action: StepAction
) -> StepOutput:
    candidate_position = copy.copy(current_position)
    if action == StepAction.UP:
        candidate_position.y -= 1
    elif action == StepAction.DOWN:
        candidate_position.y += 1
    elif action == StepAction.LEFT:
        candidate_position.x -= 1
    elif action == StepAction.RIGHT:
        candidate_position.x += 1

    outcome = _get_outcome(grid, obstacles, candidate_position, action)
    if outcome in [StepOutcome.OUT_OF_BOUNDS, StepOutcome.BLOCKED]:
        candidate_position = current_position

    return StepOutput(candidate_position, outcome)


def choose_action(
    current_position: Point,
    goal: Point,
) -> StepAction:
    if current_position.x < goal.x:
        return StepAction.RIGHT
    elif current_position.x > goal.x:
        return StepAction.LEFT
    elif current_position.y < goal.y:
        return StepAction.DOWN
    elif current_position.y > goal.y:
        return StepAction.UP
    return StepAction.WAIT