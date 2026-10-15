# Execute the selected route and inspect actual outcomes

from copy import copy

from data.data_models import StepOutput
from data.models import StepAction, StepOutcome

def _get_outcome(grid: tuple[int, int], obstacles: set[tuple[int, int]], position: tuple[int, int], action: StepAction) -> StepOutcome:
    if action == StepAction.WAIT:
        return StepOutcome.WAITED

    width, height = grid
    x, y = position
    if x >= width or y >= height or x < 0 or y < 0:
        return StepOutcome.OUT_OF_BOUNDS

    for obstacle in obstacles:
        if position == obstacle:
            return StepOutcome.BLOCKED

    return StepOutcome.MOVED


def step(
    grid: tuple[int, int],
    obstacles: set[tuple[int, int]],
    current_position: tuple[int, int],
    action: StepAction
) -> StepOutput:
    candidate_position = copy(current_position)
    x, y = candidate_position
    if action == StepAction.UP:
        candidate_position = (x, y - 1)
    elif action == StepAction.DOWN:
        candidate_position = (x, y + 1)
    elif action == StepAction.LEFT:
        candidate_position = (x - 1, y)
    elif action == StepAction.RIGHT:
        candidate_position = (x + 1, y)

    outcome = _get_outcome(grid, obstacles, candidate_position, action)
    if outcome in [StepOutcome.OUT_OF_BOUNDS, StepOutcome.BLOCKED]:
        candidate_position = current_position

    return StepOutput(candidate_position, outcome)


def choose_action(
    current_position: tuple[int, int],
    goal: tuple[int, int],
) -> StepAction:
    x, y = current_position
    goal_x, goal_y = goal
    if x < goal_x:
        return StepAction.RIGHT
    elif x > goal_x:
        return StepAction.LEFT
    elif y < goal_y:
        return StepAction.DOWN
    elif y > goal_y:
        return StepAction.UP
    return StepAction.WAIT
