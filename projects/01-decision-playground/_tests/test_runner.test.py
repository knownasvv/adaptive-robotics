import pytest

from data.data_models import NavigationOutput, StepOutput, PathExecutionOutput
from data.models import NavigationState, StepAction, StepOutcome, StoppingReason
from engine.runner import step, choose_action, action_between, execute_path, navigate

GRID = (4, 3)
DETOUR = [(1, 1), (1, 0), (2, 0), (3, 0), (3, 1)]


@pytest.mark.parametrize(
    "position, action, expected",
    [
        pytest.param(
            (1, 1),
            StepAction.RIGHT,
            StepOutput((1, 1), StepOutcome.BLOCKED),
            id="step-1-right",
        ),
        pytest.param(
            (1, 1),
            StepAction.DOWN,
            StepOutput((1, 2), StepOutcome.MOVED),
            id="step-2-down",
        ),
        pytest.param(
            (1, 2),
            StepAction.DOWN,
            StepOutput((1, 2), StepOutcome.OUT_OF_BOUNDS),
            id="step-3-down",
        ),
        pytest.param(
            (1, 2),
            StepAction.WAIT,
            StepOutput((1, 2), StepOutcome.WAITED),
            id="step-4-wait",
        ),
        pytest.param(
            (1, 2),
            StepAction.LEFT,
            StepOutput((0, 2), StepOutcome.MOVED),
            id="step-5-left",
        ),
        pytest.param(
            (0, 2),
            StepAction.LEFT,
            StepOutput((0, 2), StepOutcome.OUT_OF_BOUNDS),
            id="step-6-left",
        ),
        pytest.param(
            (0, 2),
            StepAction.RIGHT,
            StepOutput((1, 2), StepOutcome.MOVED),
            id="step-7-right",
        ),
        pytest.param(
            (1, 2),
            StepAction.RIGHT,
            StepOutput((2, 2), StepOutcome.MOVED),
            id="step-8-right",
        ),
        pytest.param(
            (2, 2),
            StepAction.RIGHT,
            StepOutput((3, 2), StepOutcome.MOVED),
            id="step-9-right",
        ),
        pytest.param(
            (3, 2),
            StepAction.RIGHT,
            StepOutput((3, 2), StepOutcome.OUT_OF_BOUNDS),
            id="step-10-right",
        ),
        pytest.param(
            (3, 2),
            StepAction.UP,
            StepOutput((3, 1), StepOutcome.MOVED),
            id="step-11-up",
        ),
        pytest.param(
            (3, 1),
            StepAction.UP,
            StepOutput((3, 0), StepOutcome.MOVED),
            id="step-12-up",
        ),
        pytest.param(
            (3, 0),
            StepAction.UP,
            StepOutput((3, 0), StepOutcome.OUT_OF_BOUNDS),
            id="step-13-up",
        ),
    ],
)
def test_step(position, action, expected):
    assert step(GRID, {(2, 1)}, position, action) == expected


@pytest.mark.parametrize(
    "case",
    [
        pytest.param(
            {
                "name": "goal reached",
                "start": (0, 0),
                "goal": (3, 2),
                "obstacles": set(),
                "expected_step_count": 5,
                "expected_stopping_reason": StoppingReason.GOAL_REACHED,
                "final_position": (3, 2),
                "step_count_budget": 5,
            },
            id="goal reached",
        ),
        pytest.param(
            {
                "name": "custom limit reached",
                "start": (0, 0),
                "goal": (3, 2),
                "obstacles": set(),
                "expected_step_count": 4,
                "expected_stopping_reason": StoppingReason.STEP_LIMIT,
                "final_position": (3, 1),
                "step_count_budget": 4,
            },
            id="custom limit reached",
        ),
        pytest.param(
            {
                "name": "goal reached with no step",
                "start": (3, 2),
                "goal": (3, 2),
                "obstacles": set(),
                "expected_step_count": 0,
                "expected_stopping_reason": StoppingReason.GOAL_REACHED,
                "final_position": (3, 2),
            },
            id="goal reached with no step",
        ),
        pytest.param(
            {
                "name": "limit reached",
                "start": (1, 1),
                "goal": (3, 1),
                "obstacles": {(2, 1)},
                "expected_step_count": 10,
                "expected_stopping_reason": StoppingReason.STEP_LIMIT,
                "final_position": (1, 1),
            },
            id="limit reached",
        ),
        pytest.param(
            {
                "name": "goal reached from the bottom right corner",
                "start": (3, 2),
                "goal": (0, 0),
                "obstacles": set(),
                "expected_step_count": 5,
                "expected_stopping_reason": StoppingReason.GOAL_REACHED,
                "final_position": (0, 0),
            },
            id="goal reached from the bottom right corner",
        ),
    ],
)
def test_choose_action(case):
    position = case["start"]
    step_count = 0
    while step_count < case.get("step_count_budget", 10) and position != case["goal"]:
        action = choose_action(position, case["goal"])
        output = step(GRID, case["obstacles"], position, action)
        position = output.position
        step_count += 1
    reason = (
        StoppingReason.GOAL_REACHED
        if position == case["goal"]
        else StoppingReason.STEP_LIMIT
    )
    assert step_count == case["expected_step_count"]
    assert position == case["final_position"]
    assert reason == case["expected_stopping_reason"]


@pytest.mark.parametrize(
    "current, target, expected",
    [
        pytest.param((1, 1), (1, 0), StepAction.UP, id="up"),
        pytest.param((1, 1), (1, 2), StepAction.DOWN, id="down"),
        pytest.param((1, 1), (0, 1), StepAction.LEFT, id="left"),
        pytest.param((1, 1), (2, 1), StepAction.RIGHT, id="right"),
    ],
)
def test_action_between(current, target, expected):
    assert action_between(current, target) == expected


@pytest.mark.parametrize(
    "current, target",
    [
        pytest.param((1, 1), (1, 1), id="no movement"),
        pytest.param((1, 1), (2, 2), id="diagonal movement"),
        pytest.param((1, 1), (3, 1), id="more than one cell"),
    ],
)
def test_action_between_rejects_invalid_segment(current, target):
    with pytest.raises(ValueError):
        action_between(current, target)


@pytest.mark.parametrize(
    "case",
    [
        pytest.param(
            {
                "name": "reach goal exactly at budget",
                "path": DETOUR,
                "obstacles": {(2, 1)},
                "budget": 4,
                "position": (3, 1),
                "ticks": 4,
                "reason": StoppingReason.GOAL_REACHED,
            },
            id="reach goal exactly at budget",
        ),
        pytest.param(
            {
                "name": "budget expires before arrival",
                "path": DETOUR,
                "obstacles": {(2, 1)},
                "budget": 3,
                "position": (3, 0),
                "ticks": 3,
                "reason": StoppingReason.STEP_LIMIT,
            },
            id="budget expires before arrival",
        ),
        pytest.param(
            {
                "name": "already at goal with zero budget",
                "path": [(1, 1)],
                "obstacles": set(),
                "budget": 0,
                "position": (1, 1),
                "ticks": 0,
                "reason": StoppingReason.GOAL_REACHED,
            },
            id="already at goal with zero budget",
        ),
        pytest.param(
            {
                "name": "zero budget with movement remaining",
                "path": DETOUR,
                "obstacles": {(2, 1)},
                "budget": 0,
                "position": (1, 1),
                "ticks": 0,
                "reason": StoppingReason.STEP_LIMIT,
            },
            id="zero budget with movement remaining",
        ),
        pytest.param(
            {
                "name": "new obstacle blocks second movement",
                "path": DETOUR,
                "obstacles": {(2, 1), (2, 0)},
                "budget": 4,
                "position": (1, 0),
                "ticks": 2,
                "reason": StoppingReason.EXECUTION_FAILED,
            },
            id="new obstacle blocks second movement",
        ),
        pytest.param(
            {
                "name": "failure on final permitted action",
                "path": DETOUR,
                "obstacles": {(2, 1), (2, 0)},
                "budget": 2,
                "position": (1, 0),
                "ticks": 2,
                "reason": StoppingReason.EXECUTION_FAILED,
            },
            id="failure on final permitted action",
        ),
    ],
)
def test_execute_path(case):
    path = case["path"].copy()
    obstacles = case["obstacles"].copy()
    original_path = path.copy()
    original_obstacles = obstacles.copy()
    result = execute_path(GRID, obstacles, path, case["budget"])
    assert result.position == case["position"]
    assert result.executed_count == case["ticks"]
    assert result.stopping_reason == case["reason"]
    assert path == original_path
    assert obstacles == original_obstacles


@pytest.mark.parametrize(
    "case",
    [
        pytest.param(
            {
                "name": "clear route",
                "start": (0, 0),
                "goal": (3, 2),
                "obstacles": set(),
                "budget": 10,
                "expected_result": NavigationOutput(
                    execution=PathExecutionOutput(
                        (3, 2), 5, StoppingReason.GOAL_REACHED
                    ),
                    state_history=[
                        NavigationState.IDLE,
                        NavigationState.PLANNING,
                        NavigationState.EXECUTING,
                        NavigationState.SUCCEEDED,
                    ]
                ),
            },
            id="clear route",
        ),
        pytest.param(
            {
                "name": "detour",
                "start": (1, 1),
                "goal": (3, 1),
                "obstacles": {(2, 1)},
                "budget": 4,
                "expected_result": NavigationOutput(
                    execution=PathExecutionOutput(
                        (3, 1), 4, StoppingReason.GOAL_REACHED
                    ),
                    state_history=[
                        NavigationState.IDLE,
                        NavigationState.PLANNING,
                        NavigationState.EXECUTING,
                        NavigationState.SUCCEEDED,
                    ]
                ),
            },
            id="detour",
        ),
        pytest.param(
            {
                "name": "incomplete detour",
                "start": (1, 1),
                "goal": (3, 1),
                "obstacles": {(2, 1)},
                "budget": 3,
                "expected_result": NavigationOutput(
                    execution=PathExecutionOutput(
                        (3, 0), 3, StoppingReason.STEP_LIMIT
                    ),
                    state_history=[
                        NavigationState.IDLE,
                        NavigationState.PLANNING,
                        NavigationState.EXECUTING,
                        NavigationState.FAILED,
                    ]
                ),
            },
            id="incomplete detour",
        ),
        pytest.param(
            {
                "name": "already complete",
                "start": (1, 1),
                "goal": (1, 1),
                "obstacles": set(),
                "budget": 0,
                "expected_result": NavigationOutput(
                    execution=PathExecutionOutput(
                        (1, 1), 0, StoppingReason.GOAL_REACHED
                    ),
                    state_history=[
                        NavigationState.IDLE,
                        NavigationState.PLANNING,
                        NavigationState.SUCCEEDED,
                    ]
                ),
            },
            id="already complete",
        ),
        pytest.param(
            {
                "name": "no movement budget",
                "start": (1, 1),
                "goal": (3, 1),
                "obstacles": {(2, 1)},
                "budget": 0,
                "expected_result": NavigationOutput(
                    execution=PathExecutionOutput(
                        (1, 1), 0, StoppingReason.STEP_LIMIT
                    ),
                    state_history=[
                        NavigationState.IDLE,
                        NavigationState.PLANNING,
                        NavigationState.EXECUTING,
                        NavigationState.FAILED,
                    ]
                ),
            },
            id="no movement budget",
        ),
        pytest.param(
            {
                "name": "enclosed start",
                "start": (1, 1),
                "goal": (3, 1),
                "obstacles": {(1, 0), (1, 2), (0, 1), (2, 1)},
                "budget": 10,
                "expected_result": NavigationOutput(
                    execution=PathExecutionOutput(
                        (1, 1), 0, StoppingReason.NO_PATH
                    ),
                    state_history=[
                        NavigationState.IDLE,
                        NavigationState.PLANNING,
                        NavigationState.FAILED,
                    ]
                ),
            },
            id="enclosed start",
        ),
        pytest.param(
            {
                "start": (1, 1),
                "goal": (3, 1),
                "obstacles": {(2, 1)},
                "budget": 4,
                "execution_stub": PathExecutionOutput(
                    position=(1, 0),
                    executed_count=2,
                    stopping_reason=StoppingReason.EXECUTION_FAILED,
                ),
                "expected_result": NavigationOutput(
                    execution=PathExecutionOutput(
                        position=(1, 0),
                        executed_count=2,
                        stopping_reason=StoppingReason.EXECUTION_FAILED,
                    ),
                    state_history=[
                        NavigationState.IDLE,
                        NavigationState.PLANNING,
                        NavigationState.EXECUTING,
                        NavigationState.FAILED,
                    ],
                ),
            },
            id="movement failure during navigation",
        )
    ],
)
def test_navigate(case, monkeypatch):
    if "execution_stub" in case:
        def fake_execute_path(**kwargs):
            return case["execution_stub"]

        monkeypatch.setattr(
            "engine.runner.execute_path",
            fake_execute_path,
        )

    result = navigate(
        grid=GRID, 
        obstacles=case["obstacles"], 
        start=case["start"],
        goal=case["goal"], 
        action_budget=case["budget"],
    )
    assert result == case["expected_result"]