# Explore possible routes using the map
# * Does not move the robot or consume an action tick
# * A neighboring cell must satisfy all three conditions:
#   1. It is exactly one horizontal or vertical step away.
#   2. It lies inside the grid.
#   3. It is not occupied.
# * There are no diagonal connections

# Requirements:
# - Consider candidates in this fixed order: UP, DOWN, LEFT, RIGHT.
# - Return only allowed positions, preserving that order.
# - Return an empty list when no movement is possible.
# - Do not include the starting position.
# - Do not modify the input position or obstacles.
# - Do not choose a route or consider the goal yet.
# - Assume the input position is valid and unoccupied.
def get_neighbors(
    grid: tuple[int, int],
    obstacles: list[tuple[int, int]],
    position: tuple[int, int]
) -> list[tuple[int, int]]:
    width, height = grid
    x, y = position
    candidate_neighbors: list[tuple[int, int]] = [
        (x, y - 1), # up
        (x, y + 1), # down
        (x - 1, y), # left
        (x + 1, y), # right
    ]
    valid_neighbors: list[tuple[int, int]] = []
    for neighbor in candidate_neighbors:
        neighbor_x, neighbor_y = neighbor
        if (neighbor not in obstacles
            and neighbor_x >= 0
            and neighbor_y >= 0
            and neighbor_x < width
            and neighbor_y < height):
            valid_neighbors.append(neighbor)

    return valid_neighbors
