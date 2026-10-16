import unittest

from data.data_models import StepOutput, PathExecutionOutput
from data.models import StepAction, StepOutcome, StoppingReason
from engine.runner import step, choose_action, action_between, execute_path, navigate


GRID = (4, 3)

class TestRunner(unittest.TestCase):
    def test_step(self):
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
        for index, case in enumerate(cases):
            action = case['action']
            expected_output = case['expected_output']

            with self.subTest(index=index):
                output = step(
                    grid=GRID,
                    obstacles=obstacles,
                    current_position=position,
                    action=action)
                position = output.position
                i += 1
                self.assertEqual(output, expected_output)

    def test_choose_action(self):
        cases = [
            {
                'name': 'goal reached',
                'start': (0, 0),
                'goal': (3, 2),
                'obstacles': set(),
                'expected_step_count': 5,
                'expected_stopping_reason': StoppingReason.GOAL_REACHED,
                'final_position': (3, 2),
                'step_count_budget': 5,
            },
            {
                'name': 'custom limit reached',
                'start': (0, 0),
                'goal': (3, 2),
                'obstacles': set(),
                'expected_step_count': 4,
                'expected_stopping_reason': StoppingReason.STEP_LIMIT,
                'final_position': (3, 1),
                'step_count_budget': 4,
            },
            {
                'name': 'goal reached with no step',
                'start': (3, 2),
                'goal': (3, 2),
                'obstacles': set(),
                'expected_step_count': 0,
                'expected_stopping_reason': StoppingReason.GOAL_REACHED,
                'final_position': (3, 2),
            },
            {
                'name': 'limit reached',
                'start': (1, 1),
                'goal': (3, 1),
                'obstacles': {(2, 1)},
                'expected_step_count': 10,
                'expected_stopping_reason': StoppingReason.STEP_LIMIT,
                'final_position': (1, 1),
            },
            {
                'name': 'goal reached from the bottom right corner',
                'start': (3, 2),
                'goal': (0, 0),
                'obstacles': set(),
                'expected_step_count': 5,
                'expected_stopping_reason': StoppingReason.GOAL_REACHED,
                'final_position': (0, 0),
            },
        ]

        for index, case in enumerate(cases):
            name = case['name']
            start = case['start']
            goal = case['goal']
            obstacles = case['obstacles']
            expected_step_count = case['expected_step_count']
            expected_stopping_reason = case['expected_stopping_reason']
            final_position = case['final_position']
            step_count_budget = case.get('step_count_budget', 10)

            step_count = 0
            current_position = start
            with self.subTest(case=name, index=index):
                while step_count < step_count_budget:
                    if current_position == goal:
                        break

                    action = choose_action(current_position, goal)
                    output = step(GRID, obstacles, current_position, action)
                    current_position = output.position

                    step_count += 1
                    
                stopping_reason = StoppingReason.GOAL_REACHED if current_position == goal else StoppingReason.STEP_LIMIT

                self.assertEqual(step_count, expected_step_count, step_count)
                self.assertEqual(current_position, final_position, current_position)
                self.assertEqual(stopping_reason, expected_stopping_reason, stopping_reason)

    def test_action_between(self):
        cases = [
            ('up', (1, 1), (1, 0), StepAction.UP),
            ('down', (1, 1), (1, 2), StepAction.DOWN),
            ('left', (1, 1), (0, 1), StepAction.LEFT),
            ('right', (1, 1), (2, 1), StepAction.RIGHT),
        ]

        for index, (name, current, target, expected) in enumerate(cases):
            with self.subTest(case=name, index=index):
                actual = action_between(current, target)
                self.assertEqual(actual, expected, (f'{current} -> {target}: expected {expected}, got {actual}'))

        invalid_cases = [
            ('no movement', (1, 1), (1, 1)),  # No movement
            ('diagonal movement', (1, 1), (2, 2)),  # Diagonal movement
            ('more than one cell', (1, 1), (3, 1)),  # More than one cell
        ]

        for index, (name, current, target) in enumerate(invalid_cases):
            with self.subTest(case='invalid case - ' + name, index=index):
                try:
                    actual = action_between(current, target)
                except Exception as ex:
                    self.assertIsInstance(ex, ValueError, f'Expected ValueError for {current} -> {target}')
            
    def test_execute_path(self):
        detour = [(1, 1), (1, 0), (2, 0), (3, 0), (3, 1)]

        cases = [
            {
                'name': 'reach goal exactly at budget',
                'path': detour,
                'obstacles': {(2, 1)},
                'budget': 4,
                'position': (3, 1),
                'ticks': 4,
                'reason': StoppingReason.GOAL_REACHED,
            },
            {
                'name': 'budget expires before arrival',
                'path': detour,
                'obstacles': {(2, 1)},
                'budget': 3,
                'position': (3, 0),
                'ticks': 3,
                'reason': StoppingReason.STEP_LIMIT,
            },
            {
                'name': 'already at goal with zero budget',
                'path': [(1, 1)],
                'obstacles': set(),
                'budget': 0,
                'position': (1, 1),
                'ticks': 0,
                'reason': StoppingReason.GOAL_REACHED,
            },
            {
                'name': 'zero budget with movement remaining',
                'path': detour,
                'obstacles': {(2, 1)},
                'budget': 0,
                'position': (1, 1),
                'ticks': 0,
                'reason': StoppingReason.STEP_LIMIT,
            },
            {
                'name': 'new obstacle blocks second movement',
                'path': detour,
                'obstacles': {(2, 1), (2, 0)},
                'budget': 4,
                'position': (1, 0),
                'ticks': 2,
                'reason': StoppingReason.EXECUTION_FAILED,
            },
            {
                'name': 'failure on final permitted action',
                'path': detour,
                'obstacles': {(2, 1), (2, 0)},
                'budget': 2,
                'position': (1, 0),
                'ticks': 2,
                'reason': StoppingReason.EXECUTION_FAILED,
            },
        ]

        for index, case in enumerate(cases):
            name = case['name']
            path = case['path'].copy()
            obstacles = case['obstacles'].copy()
            original_path = path.copy()
            original_obstacles = obstacles.copy()

            with self.subTest(case=name, index=index):
                result = execute_path(
                    grid=GRID,
                    obstacles=obstacles,
                    path=path,
                    action_budget=case['budget'],
                )

                self.assertEqual(result.position, case['position'], result)
                self.assertEqual(result.executed_count, case['ticks'], result)
                self.assertEqual(result.stopping_reason, case['reason'], result)

                self.assertEqual(path, original_path, result)
                self.assertEqual(obstacles, original_obstacles, result)
            
    def test_navigate(self):
        
        cases = [
            {
                'name': 'clear route',
                'start': (0, 0),
                'goal': (3, 2),
                'obstacles': set(),
                'budget': 10,
                'expected_result': PathExecutionOutput((3, 2), 5, StoppingReason.GOAL_REACHED)
            }, {
                'name': 'detour',
                'start': (1, 1),
                'goal': (3, 1),
                'obstacles': {(2, 1)},
                'budget': 4,
                'expected_result': PathExecutionOutput((3, 1), 4, StoppingReason.GOAL_REACHED)
            }, {
                'name': 'incomplete detour',
                'start': (1, 1),
                'goal': (3, 1),
                'obstacles': {(2, 1)},
                'budget': 3,
                'expected_result': PathExecutionOutput((3, 0), 3, StoppingReason.STEP_LIMIT)
            }, {
                'name': 'already complete',
                'start': (1, 1),
                'goal': (1, 1),
                'obstacles': set(),
                'budget': 0,
                'expected_result': PathExecutionOutput((1, 1), 0, StoppingReason.GOAL_REACHED)
            },
            {
                'name': 'no movement budget',
                'start': (1, 1),
                'goal': (3, 1),
                'obstacles': {(2, 1)},
                'budget': 0,
                'expected_result': PathExecutionOutput((1, 1), 0, StoppingReason.STEP_LIMIT)
            }, {
                'name': 'enclosed start',
                'start': (1, 1),
                'goal': (3, 1),
                'obstacles': {(1, 0), (1, 2), (0, 1), (2, 1)},
                'budget': 10,
                'expected_result': PathExecutionOutput((1, 1), 0, StoppingReason.NO_PATH)
            }
        ]
        
        for index, case in enumerate(cases):
            name = case['name']
            start = case['start']
            goal = case['goal']
            obstacles = case['obstacles']
            budget = case['budget']
            expected_result = case['expected_result']
            
            with self.subTest(case=name, index=index):
                result = navigate(
                    grid=GRID,
                    obstacles=obstacles,
                    start=start,
                    goal=goal,
                    action_budget=budget
                )
                self.assertEqual(result, expected_result, result)


if __name__ == '__main__':
    unittest.main()