import copy

from data.data_models import Point, StepOutput
from data.models import StepAction, StepOutcome, StoppingReason

from engine.runner import step, choose_action

def test_step(): 
    grid = Point(4, 3)
    obstacles = [Point(2, 1)]
    position = Point(1, 1)

    cases = [
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
    print(f'\nTick {i} | position: {position}')
    for case in cases:
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
    grid = Point(4, 3)
    cases = [
        { 'start': Point(0, 0), 'goal': Point(3, 2), 'obstacles': [], 'expected_step_count': 5, 'expected_stopping_reason': StoppingReason.GOAL_REACHED, 'final_position': Point(3, 2), 'step_count_budget': 5 },
        { 'start': Point(0, 0), 'goal': Point(3, 2), 'obstacles': [], 'expected_step_count': 4, 'expected_stopping_reason': StoppingReason.STEP_LIMIT, 'final_position': Point(3, 1), 'step_count_budget': 4 },
        { 'start': Point(3, 2), 'goal': Point(3, 2), 'obstacles': [], 'expected_step_count': 0, 'expected_stopping_reason': StoppingReason.GOAL_REACHED, 'final_position': Point(3, 2) },
        { 'start': Point(1, 1), 'goal': Point(3, 1), 'obstacles': [Point(2, 1)], 'expected_step_count': 10, 'expected_stopping_reason': StoppingReason.STEP_LIMIT, 'final_position': Point(1, 1) },
        { 'start': Point(3, 2), 'goal': Point(0, 0), 'obstacles': [], 'expected_step_count': 5, 'expected_stopping_reason': StoppingReason.GOAL_REACHED, 'final_position': Point(0, 0) },

    ]
    for case in cases:
        start = case['start']
        goal = case['goal']
        obstacles = case['obstacles']
        expected_step_count = case['expected_step_count']
        expected_stopping_reason = case['expected_stopping_reason']
        final_position = case['final_position']
        step_count_budget = case.get('step_count_budget', 10)
        
        step_count = 0
        current_position = copy.copy(start)
        print(f'\nTick {step_count} | start: {start}, goal: {goal}, obstacles: {obstacles}')
        while step_count < step_count_budget:
            if current_position == goal:
                break
            
            action = choose_action(current_position, goal)
            output = step(grid, obstacles, current_position, action)
            current_position = output.position
            
            step_count += 1
            distance = abs(goal.x - current_position.x) + abs(goal.y - current_position.y)
            print(f'Tick {step_count} | action: {action.name}, outcome: {output.outcome.name}, ' \
                  f'position: {output.position}, distance: {distance}')
            
        stopping_reason = StoppingReason.GOAL_REACHED if current_position == goal else StoppingReason.STEP_LIMIT
        print(f'   Stopping reason: {stopping_reason}')

        assert step_count == expected_step_count
        assert current_position == final_position
        assert stopping_reason == expected_stopping_reason