from data.data_models import StepOutput
from data.models import StepAction, StepOutcome, StoppingReason

from engine.planner import get_neighbors, find_path
from engine.runner import step, choose_action


# planner
def test_find_path():
    print(f'\n================= test_find_path() =================')

    grid = (4, 3)

    cases = [
        {
            "start": (1, 1),
            "goal": (3, 1),
            "obstacles": {(2, 1)},
            "expected_return": [(1, 1), (1, 0), (2, 0), (3, 0), (3, 1)],
        },
        {
            'start': (1, 1),
            'goal': (1, 1),
            "obstacles": set(),
            "expected_return": [(1, 1)],
        },
        {
            'start': (1, 1),
            'goal': (3, 1),
            'obstacles': {(1, 0), (1, 2), (0, 1), (2, 1)},
            'expected_return': None
        }
    ]

    for case in cases:
        start = case['start']
        goal = case['goal']
        obstacles = case['obstacles']
        expected_return = case['expected_return']
        
        path = find_path(
            grid=grid,
            obstacles=obstacles,
            start=start,
            goal=goal
        )
        print(f'returned path: {path}')
        assert path == expected_return


def test_get_neighbors():
    print(f'\n================= test_get_neighbors() =================')

    grid = (4, 3)

    cases = [
        { # 1. Exclude an occupied neighbor
            'position': (1, 1),
            'obstacles': {(2, 1)},
            'expected_neighbors': [(1, 0), (1, 2), (0, 1)]
        }, { # 2. Exclude candidates beyond two boundaries
            'position': (0, 0),
            'obstacles': set(),
            'expected_neighbors': [(0, 1), (1, 0)]
        }, { # 3. Exclude the opposite corner
            'position': (3, 2),
            'obstacles': set(),
            'expected_neighbors': [(3, 1), (2, 2)]
        }, { # 4. A completely enclosed position
            'position': (1, 1),
            'obstacles': {(1, 0), (1, 2), (0, 1), (2, 1)},
            'expected_neighbors': []
        }
    ]

    for index, case in enumerate(cases):
        print(f'\n----- Case {index} -----')

        position = case['position']
        obstacles = case['obstacles']
        expected_neighbors = case['expected_neighbors']
        original_position = position
        original_obstacles = obstacles.copy()

        neighbors = get_neighbors(
            grid=grid,
            obstacles=obstacles,
            position=position
        )
        print(f'  neighbors: {neighbors}, expected neighbors: {expected_neighbors}')
        assert neighbors == expected_neighbors
        assert position == original_position
        assert obstacles == original_obstacles
        assert len(set(neighbors)) == len(neighbors)


# runner
def test_step():
    print(f'\n================= test_step() =================')

    grid = (4, 3)
    obstacles = {(2, 1)}
    position = (1, 1)

    cases = [
        { 'action': StepAction.RIGHT, 'expected_output': StepOutput((1, 1), StepOutcome.BLOCKED) },         # move into obstacle
        { 'action': StepAction.DOWN,  'expected_output': StepOutput((1, 2), StepOutcome.MOVED) },           # move into a free cell
        { 'action': StepAction.DOWN,  'expected_output': StepOutput((1, 2), StepOutcome.OUT_OF_BOUNDS)  },  # move down from the bottom edge
        { 'action': StepAction.WAIT,  'expected_output': StepOutput((1, 2), StepOutcome.WAITED)  },         # wait in a valid cell
        { 'action': StepAction.LEFT,  'expected_output': StepOutput((0, 2), StepOutcome.MOVED)  },
        { 'action': StepAction.LEFT,  'expected_output': StepOutput((0, 2), StepOutcome.OUT_OF_BOUNDS)  },  # move left from the left edge
        { 'action': StepAction.RIGHT, 'expected_output': StepOutput((1, 2), StepOutcome.MOVED)  },
        { 'action': StepAction.RIGHT, 'expected_output': StepOutput((2, 2), StepOutcome.MOVED)  },
        { 'action': StepAction.RIGHT, 'expected_output': StepOutput((3, 2), StepOutcome.MOVED)  },
        { 'action': StepAction.RIGHT, 'expected_output': StepOutput((3, 2), StepOutcome.OUT_OF_BOUNDS)  },  # move right from the right edge
        { 'action': StepAction.UP,    'expected_output': StepOutput((3, 1), StepOutcome.MOVED)  },
        { 'action': StepAction.UP,    'expected_output': StepOutput((3, 0), StepOutcome.MOVED)  },
        { 'action': StepAction.UP,    'expected_output': StepOutput((3, 0), StepOutcome.OUT_OF_BOUNDS)  },  # move up from the top edge
    ]
    i = 0
    print(f'Tick {i} | position: {position}')
    for index, case in enumerate(cases):
        print(f'\n----- Case {index} -----')
        action = case['action']
        expected_output = case['expected_output']

        output = step(
            grid=grid,
            obstacles=obstacles,
            current_position=position,
            action=action)
        position = output.position
        i += 1
        print(f'Tick {i} | after: {action.name}, output: {output}')

        # Validate
        try:
            assert output == expected_output
        except AssertionError as ex:
            print(f'   Assertion failed, expected output: {expected_output}')
            raise ex

def test_choose_action():
    print(f'\n================= test_choose_action() =================')

    grid = (4, 3)
    cases = [
        {
            "start": (0, 0),
            "goal": (3, 2),
            "obstacles": set(),
            "expected_step_count": 5,
            "expected_stopping_reason": StoppingReason.GOAL_REACHED,
            "final_position": (3, 2),
            "step_count_budget": 5,
        },
        {
            "start": (0, 0),
            "goal": (3, 2),
            "obstacles": set(),
            "expected_step_count": 4,
            "expected_stopping_reason": StoppingReason.STEP_LIMIT,
            "final_position": (3, 1),
            "step_count_budget": 4,
        },
        {
            "start": (3, 2),
            "goal": (3, 2),
            "obstacles": set(),
            "expected_step_count": 0,
            "expected_stopping_reason": StoppingReason.GOAL_REACHED,
            "final_position": (3, 2),
        },
        {
            "start": (1, 1),
            "goal": (3, 1),
            "obstacles": {(2, 1)},
            "expected_step_count": 10,
            "expected_stopping_reason": StoppingReason.STEP_LIMIT,
            "final_position": (1, 1),
        },
        {
            "start": (3, 2),
            "goal": (0, 0),
            "obstacles": set(),
            "expected_step_count": 5,
            "expected_stopping_reason": StoppingReason.GOAL_REACHED,
            "final_position": (0, 0),
        },
    ]

    for index, case in enumerate(cases):
        print(f'\n----- Case {index} -----')

        start = case['start']
        goal = case['goal']
        obstacles = case['obstacles']
        expected_step_count = case['expected_step_count']
        expected_stopping_reason = case['expected_stopping_reason']
        final_position = case['final_position']
        step_count_budget = case.get('step_count_budget', 10)

        step_count = 0
        current_position = start
        print(f'Tick {step_count} | start: {start}, goal: {goal}, obstacles: {obstacles}')
        while step_count < step_count_budget:
            if current_position == goal:
                break

            action = choose_action(current_position, goal)
            output = step(grid, obstacles, current_position, action)
            current_position = output.position

            step_count += 1
            distance = abs(goal[0] - current_position[0]) + abs(goal[1] - current_position[1])
            print(f'Tick {step_count} | action: {action.name}, outcome: {output.outcome.name}, ' \
                  f'position: {output.position}, distance: {distance}')

        stopping_reason = StoppingReason.GOAL_REACHED if current_position == goal else StoppingReason.STEP_LIMIT
        print(f'   Stopping reason: {stopping_reason}')

        assert step_count == expected_step_count
        assert current_position == final_position
        assert stopping_reason == expected_stopping_reason
