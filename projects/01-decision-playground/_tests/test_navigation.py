import pytest

from data.models import NavigationState, NavigationEvent
from engine.navigation import transition


@pytest.mark.parametrize(
    "initial_state, events, final_state",
    [
        pytest.param(
            NavigationState.IDLE,
            [
                NavigationEvent.START,
                NavigationEvent.PATH_FOUND,
                NavigationEvent.GOAL_REACHED
            ],
            NavigationState.SUCCEEDED,
            id="successful navigation",
        ),
        pytest.param(
            NavigationState.IDLE,
            [
                NavigationEvent.START,
                NavigationEvent.NO_PATH
            ],
            NavigationState.FAILED,
            id="no route"
        ),
        pytest.param(
            NavigationState.IDLE,
            [
                NavigationEvent.START,
                NavigationEvent.ALREADY_AT_GOAL
            ],
            NavigationState.SUCCEEDED,
            id='already at goal'
        ),
        pytest.param(
            NavigationState.IDLE,
            [
                NavigationEvent.START,
                NavigationEvent.PATH_FOUND,
                NavigationEvent.MOVEMENT_FAILED
            ],
            NavigationState.FAILED,
            id='movement failure'
        ),
        pytest.param(
            NavigationState.IDLE,
            [
                NavigationEvent.START,
                NavigationEvent.PATH_FOUND,
                NavigationEvent.BUDGET_EXHAUSTED
            ],
            NavigationState.FAILED,
            id='budget exhausted'
        ),
    ],
)
def test_transition(initial_state, events, final_state):
    actual_state = initial_state
    for event in events:
        actual_state = transition(actual_state, event)
    assert actual_state == final_state

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