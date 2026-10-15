# Explore possible routes using the map
# * Does not move the robot or consume an action tick
# * A neighboring cell must satisfy all three conditions:
#   1. It is exactly one horizontal or vertical step away.
#   2. It lies inside the grid.
#   3. It is not occupied.
# * There are no diagonal connections

from collections import deque


# Return the allowed connections from one cell
def get_neighbors(
    grid: tuple[int, int],
    obstacles: set[tuple[int, int]],
    position: tuple[int, int]
) -> set[tuple[int, int]]:
    width, height = grid
    x, y = position
    candidate_neighbors: set[tuple[int, int]] = {
        (x,     y - 1), # up
        (x,     y + 1), # down
        (x - 1, y),     # left
        (x + 1, y),     # right
    }
    valid_neighbors: set[tuple[int, int]] = set()
    for neighbor in candidate_neighbors:
        neighbor_x, neighbor_y = neighbor
        if (neighbor not in obstacles
            and neighbor_x >= 0
            and neighbor_y >= 0
            and neighbor_x < width
            and neighbor_y < height):
            valid_neighbors.add(neighbor)

    return valid_neighbors

# Search those connections and return a path
def find_path(
    grid: tuple[int, int],
    obstacles: set[tuple[int, int]],
    start: tuple[int, int],
    goal: tuple[int, int]
) -> set[tuple[int, int]] | None:
    raise NotImplementedError