from data.models import NavigationEvent, NavigationState


TRANSITION_RULES = {
    (NavigationState.IDLE, NavigationEvent.START): NavigationState.PLANNING,
    (NavigationState.PLANNING, NavigationEvent.PATH_FOUND): NavigationState.EXECUTING,
    (NavigationState.PLANNING, NavigationEvent.ALREADY_AT_GOAL): NavigationState.SUCCEEDED,
    (NavigationState.PLANNING, NavigationEvent.NO_PATH): NavigationState.FAILED,
    (NavigationState.EXECUTING, NavigationEvent.GOAL_REACHED): NavigationState.SUCCEEDED,
    (NavigationState.EXECUTING, NavigationEvent.MOVEMENT_FAILED): NavigationState.FAILED,
    (NavigationState.EXECUTING, NavigationEvent.BUDGET_EXHAUSTED): NavigationState.FAILED,
}

def transition(
    state: NavigationState,
    event: NavigationEvent,
) -> NavigationState:
    try:
        return TRANSITION_RULES[(state, event)]
    except KeyError:
        raise ValueError(f'invalid state and event combinations with state {state} and event {event}')
        
