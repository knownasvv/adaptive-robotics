import pytest

from data.models import NavigationState, NavigationEvent
from engine.navigation import transition


@pytest.mark.parametrize(
    "initial_state, expected_transitions",
    [
        pytest.param(
            NavigationState.IDLE,
            [
                (NavigationEvent.START, NavigationState.PLANNING),
                (NavigationEvent.PATH_FOUND, NavigationState.EXECUTING),
                (NavigationEvent.GOAL_REACHED, NavigationState.SUCCEEDED),
            ],
            id="successful navigation",
        ),
        pytest.param(
            NavigationState.IDLE,
            [
                (NavigationEvent.START, NavigationState.PLANNING),
                (NavigationEvent.NO_PATH, NavigationState.FAILED),
            ],
            id="no route",
        ),
        pytest.param(
            NavigationState.IDLE,
            [
                (NavigationEvent.START, NavigationState.PLANNING),
                (NavigationEvent.ALREADY_AT_GOAL, NavigationState.SUCCEEDED),
            ],
            id="already at goal",
        ),
        pytest.param(
            NavigationState.IDLE,
            [
                (NavigationEvent.START, NavigationState.PLANNING),
                (NavigationEvent.PATH_FOUND, NavigationState.EXECUTING),
                (NavigationEvent.MOVEMENT_FAILED, NavigationState.FAILED),
            ],
            id="movement failure",
        ),
        pytest.param(
            NavigationState.IDLE,
            [
                (NavigationEvent.START, NavigationState.PLANNING),
                (NavigationEvent.PATH_FOUND, NavigationState.EXECUTING),
                (NavigationEvent.BUDGET_EXHAUSTED, NavigationState.FAILED),
            ],
            id="budget exhausted",
        ),
    ],
)
def test_transition(initial_state, expected_transitions):
    current_state = initial_state

    for event, expected_state in expected_transitions:
        next_state = transition(current_state, event)

        assert next_state == expected_state, (
            f"{current_state.name} + {event.name}: "
            f"expected {expected_state.name}, got {next_state.name}"
        )

        current_state = next_state

@pytest.mark.parametrize(
    "state, event",
    [
        (NavigationState.IDLE, NavigationEvent.MOVEMENT_FAILED),
        (NavigationState.PLANNING, NavigationEvent.MOVEMENT_FAILED),
        (NavigationState.SUCCEEDED, NavigationEvent.START),
        (NavigationState.FAILED, NavigationEvent.PATH_FOUND)
    ]
)
def test_invalid_transition(state, event):
    with pytest.raises(ValueError):
        transition(state, event)