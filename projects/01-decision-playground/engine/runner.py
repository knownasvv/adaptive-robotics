# Execute the selected route and inspect actual outcomes

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
    candidate_position = current_position
    x, y = candidate_position
    match action:
        case StepAction.UP: candidate_position = (x, y - 1)
        case StepAction.DOWN: candidate_position = (x, y + 1)
        case StepAction.LEFT: candidate_position = (x - 1, y)
        case StepAction.RIGHT: candidate_position = (x + 1, y)

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
    match True:
        case _ if x < goal_x: return StepAction.RIGHT
        case _ if x > goal_x: return StepAction.LEFT
        case _ if y < goal_y: return StepAction.DOWN
        case _ if y > goal_y: return StepAction.UP
    return StepAction.WAIT


# Return the action connecting two adjacent cells
def action_between(
    current_position: tuple[int, int],
    next_position: tuple[int, int],
) -> StepAction:
    position_delta = tuple(a - b for a, b in zip(current_position, next_position))
    match position_delta:
        case (0, 1):  return StepAction.UP
        case (0, -1): return StepAction.DOWN
        case (1, 0):  return StepAction.LEFT
        case (-1, 0): return StepAction.RIGHT
    return StepAction.WAIT