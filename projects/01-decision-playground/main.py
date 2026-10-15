import copy

from enum import Enum
from dataclasses import dataclass


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


@dataclass
class Point:
    x: int
    y: int


@dataclass
class StepOutput:
    position: Point
    outcome: StepOutcome


def get_outcome(grid: Point, obstacles: list[Point], position: Point, action: StepAction) -> StepOutcome:
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

    outcome = get_outcome(grid, obstacles, candidate_position, action)
    if outcome in [StepOutcome.OUT_OF_BOUNDS, StepOutcome.BLOCKED]:
        candidate_position = current_position

    return StepOutput(candidate_position, outcome)


if __name__ == '__main__':

    #               x
    #         0 1 2 3
    #       ┌─────────
    # y = 0 │ . . . .
    # y = 1 │ . R # .
    # y = 2 │ . . . .
    grid = Point(4, 3)
    obstacles = [Point(2, 1)]
    position = Point(1, 1)
    steps = [
        { 'action': StepAction.RIGHT, 'expected_output': StepOutput(Point(1, 1), StepOutcome.BLOCKED) },         # move into obstacle               
        { 'action': StepAction.DOWN,  'expected_output': StepOutput(Point(1, 2), StepOutcome.MOVED) },           # move into a free cell               
        { 'action': StepAction.DOWN,  'expected_output': StepOutput(Point(1, 2), StepOutcome.OUT_OF_BOUNDS)  },  # move down from the bottom edge               
        { 'action': StepAction.WAIT,  'expected_output': StepOutput(Point(1, 2), StepOutcome.WAITED)  },         # wait in a valid cell               
        { 'action': StepAction.LEFT,  'expected_output': StepOutput(Point(0, 2), StepOutcome.MOVED)  },              
        { 'action': StepAction.LEFT,  'expected_output': StepOutput(Point(0, 2), StepOutcome.OUT_OF_BOUNDS)  },  # move left from the left edge               
        { 'action': StepAction.RIGHT, 'expected_output': StepOutput(Point(1, 2), StepOutcome.MOVED)  },
        { 'action': StepAction.RIGHT, 'expected_output': StepOutput(Point(2, 2), StepOutcome.MOVED)  },
        { 'action': StepAction.RIGHT, 'expected_output': StepOutput(Point(3, 2), StepOutcome.MOVED)  },
        { 'action': StepAction.RIGHT, 'expected_output': StepOutput(Point(3, 2), StepOutcome.OUT_OF_BOUNDS)  },  # move right from the right edge               
        { 'action': StepAction.UP,    'expected_output': StepOutput(Point(3, 1), StepOutcome.MOVED)  },
        { 'action': StepAction.UP,    'expected_output': StepOutput(Point(3, 0), StepOutcome.MOVED)  },
        { 'action': StepAction.UP,    'expected_output': StepOutput(Point(3, 0), StepOutcome.OUT_OF_BOUNDS)  },  # move up from the top edge               
    ]
    i = 0
    print(f'Tick {i}: position: {position}')
    for current_step in steps:
        action = current_step['action']
        expected_output = current_step['expected_output']
        
        output = step(
            grid=grid, 
            obstacles=obstacles, 
            current_position=position, 
            action=action)
        position = output.position
        i += 1
        print(f'Tick {i}: after {action.name}, output: {output}')
        try:
            assert output == expected_output
        except AssertionError as ex:
            print(f'   Assertion failed, expected output: {expected_output}')
            raise ex