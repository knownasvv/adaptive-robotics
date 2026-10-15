# Explore possible routes using the map
# * Does not move the robot or consume an action tick
# * A neighboring cell must satisfy all three conditions:
#   1. It is exactly one horizontal or vertical step away.
#   2. It lies inside the grid.
#   3. It is not occupied.
# * There are no diagonal connections

import copy

from dataclasses import replace
from data.data_models import Point


# Requirements:
# - Consider candidates in this fixed order: UP, DOWN, LEFT, RIGHT.
# - Return only allowed positions, preserving that order.
# - Return an empty list when no movement is possible.
# - Do not include the starting position.
# - Do not modify the input position or obstacles.
# - Do not choose a route or consider the goal yet.
# - Assume the input position is valid and unoccupied.
def get_neighbors(
    grid: Point,
    obstacles: list[Point],
    position: Point
) -> list[Point]:
    candidate_neighbors: list[Point] = [
        replace(position, y = position.y - 1), # up
        replace(position, y = position.y + 1), # down
        replace(position, x = position.x - 1), # left
        replace(position, x = position.x + 1), # right
    ]
    valid_neighbors: list[Point] = []
    for neighbor in candidate_neighbors:
        if (neighbor not in obstacles 
            and neighbor.x >= 0 
            and neighbor.y >= 0 
            and neighbor.x < grid.x 
            and neighbor.y < grid.y):
            valid_neighbors.append(neighbor)
    
    return valid_neighbors
