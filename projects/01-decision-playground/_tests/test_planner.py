import pytest

from engine.planner import get_neighbors, find_path

GRID = (4, 3)


@pytest.mark.parametrize(
    "case",
    [
        pytest.param(
            {
                "start": (1, 1),
                "goal": (3, 1),
                "obstacles": {(2, 1)},
                "expected_return": [(1, 1), (1, 0), (2, 0), (3, 0), (3, 1)],
            },
            id="detour",
        ),
        pytest.param(
            {
                "start": (1, 1),
                "goal": (1, 1),
                "obstacles": set(),
                "expected_return": [(1, 1)],
            },
            id="already-at-goal",
        ),
        pytest.param(
            {
                "start": (1, 1),
                "goal": (3, 1),
                "obstacles": {(1, 0), (1, 2), (0, 1), (2, 1)},
                "expected_return": None,
            },
            id="enclosed-start",
        ),
    ],
)
def test_find_path(case):
    path = find_path(GRID, case["obstacles"], case["start"], case["goal"])
    assert path == case["expected_return"]


@pytest.mark.parametrize(
    "case",
    [
        pytest.param(
            {
                "position": (1, 1),
                "obstacles": {(2, 1)},
                "expected_neighbors": [(1, 0), (1, 2), (0, 1)],
            },
            id="occupied-neighbor",
        ),
        pytest.param(
            {
                "position": (0, 0),
                "obstacles": set(),
                "expected_neighbors": [(0, 1), (1, 0)],
            },
            id="top-left",
        ),
        pytest.param(
            {
                "position": (3, 2),
                "obstacles": set(),
                "expected_neighbors": [(3, 1), (2, 2)],
            },
            id="bottom-right",
        ),
        pytest.param(
            {
                "position": (1, 1),
                "obstacles": {(1, 0), (1, 2), (0, 1), (2, 1)},
                "expected_neighbors": [],
            },
            id="enclosed",
        ),
    ],
)
def test_get_neighbors(case):
    position = case["position"]
    obstacles = case["obstacles"].copy()
    original_obstacles = obstacles.copy()
    neighbors = get_neighbors(GRID, obstacles, position)
    assert neighbors == case["expected_neighbors"]
    assert position == case["position"]
    assert obstacles == original_obstacles
    assert len(set(neighbors)) == len(neighbors)
