# Explore possible routes using the map
# * Does not move the robot or consume an action tick
# * A neighboring cell must satisfy all three conditions:
#   1. It is exactly one horizontal or vertical step away.
#   2. It lies inside the grid.
#   3. It is not occupied.
# * There are no diagonal connections
import logging


from collections import deque


# Return the allowed connections from one cell
def get_neighbors(
    grid: tuple[int, int],
    obstacles: set[tuple[int, int]],
    position: tuple[int, int]
) -> list[tuple[int, int]]:
    width, height = grid
    x, y = position
    candidate_neighbors: list[tuple[int, int]] = [
        (x,     y - 1), # up
        (x,     y + 1), # down
        (x - 1, y),     # left
        (x + 1, y),     # right
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


def _reconstruct_path(came_from, goal) -> list[tuple[int, int]]:
    path = deque([goal])
    cursor = came_from[goal]
    
    while cursor is not None:
        path.append(cursor)
        cursor = came_from[cursor]
    
    path.reverse()
    return list(path)
        

# Search those connections and return a path
def find_path(
    grid: tuple[int, int],
    obstacles: set[tuple[int, int]],
    start: tuple[int, int],
    goal: tuple[int, int]
) -> list[tuple[int, int]] | None:
    frontier = deque([start])
    came_from: dict[
        tuple[int, int], 
        tuple[int, int] | None
    ] = { start: None }
    
    while frontier:
        current = frontier.popleft()
        
        if current == goal:
            path = _reconstruct_path(came_from, goal)
            logging.debug(f'  [find_path()] path found: {path}')
            return path
        
        neighbors = get_neighbors(
            grid=grid,
            obstacles=obstacles,
            position=current
        )
        for neighbor in neighbors: 
            if neighbor in came_from:
                continue
            
            came_from[neighbor] = current
            frontier.append(neighbor)
    
    return None