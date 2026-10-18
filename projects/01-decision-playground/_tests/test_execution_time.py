"""Execution time is global; action counts and budgets are local to each call."""

import pytest

from data.data_models import PathExecutionOutput
from data.models import NavigationState, StoppingReason
from engine.runner import execute_path, navigate


@pytest.mark.parametrize(
    "path, start_tick, budget, snapshots, expected, expected_ticks",
    [
        pytest.param(
            [(1, 0), (2, 0), (3, 0)],
            2,
            2,
            {2: set(), 3: set()},
            PathExecutionOutput((3, 0), 2, StoppingReason.GOAL_REACHED),
            [2, 3],
            id="offset ticks preserve local action count",
        ),
        pytest.param(
            [(1, 0), (2, 0)],
            2,
            3,
            {2: {(2, 0)}},
            PathExecutionOutput((1, 0), 1, StoppingReason.EXECUTION_FAILED),
            [2],
            id="blocked attempt consumes one local action",
        ),
        pytest.param(
            [(1, 0), (2, 0), (3, 0)],
            10,
            1,
            {10: set()},
            PathExecutionOutput((2, 0), 1, StoppingReason.STEP_LIMIT),
            [10],
            id="budget is independent of starting tick",
        ),
        pytest.param(
            [(1, 0), (2, 0)],
            2,
            0,
            {},
            PathExecutionOutput((1, 0), 0, StoppingReason.STEP_LIMIT),
            [],
            id="zero budget does not advance time",
        ),
        pytest.param(
            [(1, 0)],
            2,
            3,
            {},
            PathExecutionOutput((1, 0), 0, StoppingReason.GOAL_REACHED),
            [],
            id="completed path does not advance time",
        ),
    ],
)
def test_execute_path_start_tick(
    path, start_tick, budget, snapshots, expected, expected_ticks
):
    observed_ticks = []

    def obstacles_at(tick):
        observed_ticks.append(tick)
        # Unexpected ticks fail immediately rather than silently using old data.
        return snapshots[tick].copy()

    result = execute_path(
        grid=(4, 3),
        obstacles=set(),
        path=path,
        action_budget=budget,
        obstacles_at=obstacles_at,
        start_tick=start_tick,
    )

    assert result == expected
    assert observed_ticks == expected_ticks


def test_two_execution_calls_share_time_and_budget():
    snapshots = {
        0: {(2, 1)},
        1: {(2, 1), (2, 0)},
        2: {(2, 1)},
        3: {(2, 1)},
        4: {(2, 1)},
    }
    observed_ticks = []

    def obstacles_at(tick):
        observed_ticks.append(tick)
        return snapshots[tick].copy()

    initial_budget = 8
    first = execute_path(
        grid=(4, 3),
        obstacles={(2, 1)},
        path=[(1, 1), (1, 0), (2, 0), (3, 0), (3, 1)],
        action_budget=initial_budget,
        obstacles_at=obstacles_at,
        # Omitted start_tick must default to zero.
    )
    assert first == PathExecutionOutput((1, 0), 2, StoppingReason.EXECUTION_FAILED)
    assert observed_ticks == [0, 1]

    # Explicitly resume a route; this test does not implement a recovery policy.
    second = execute_path(
        grid=(4, 3),
        obstacles={(2, 1)},
        path=[first.position, (2, 0), (3, 0), (3, 1)],
        action_budget=initial_budget - first.executed_count,
        start_tick=first.executed_count,
        obstacles_at=obstacles_at,
    )
    assert second == PathExecutionOutput((3, 1), 3, StoppingReason.GOAL_REACHED)
    assert observed_ticks == [0, 1, 2, 3, 4]
    assert initial_budget - first.executed_count - second.executed_count == 3


def test_navigate_forwards_start_tick_without_consuming_budget():
    # Only current/future snapshots exist: querying tick zero must fail.
    snapshots = {2: set(), 3: set()}
    observed_ticks = []

    def obstacles_at(tick):
        observed_ticks.append(tick)
        return snapshots[tick].copy()

    result = navigate(
        grid=(4, 3),
        obstacles=set(),
        start=(1, 0),
        goal=(3, 0),
        action_budget=2,
        obstacles_at=obstacles_at,
        start_tick=2,
    )

    assert observed_ticks == [2, 3]
    assert result.execution == PathExecutionOutput(
        position=(3, 0),
        executed_count=2,
        stopping_reason=StoppingReason.GOAL_REACHED,
    )
    assert result.state_history == [
        NavigationState.IDLE,
        NavigationState.PLANNING,
        NavigationState.EXECUTING,
        NavigationState.SUCCEEDED,
    ]
