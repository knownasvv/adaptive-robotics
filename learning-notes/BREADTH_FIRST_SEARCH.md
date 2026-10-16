# Breadth-First Search

Learning objective: Understand how breadth-first search (BFS) explores a map without repeatedly visiting the same cells.

BFS needs two records:
1. A queue of discovered cells waiting to be explored
    A queue follows first in, first out. New cells join the back; exploration takes the cell at the front.
    This ordering is what makes BFS explore nearby cells before more distant ones.

2. A record of discovered cells and their parents
    A cell’s parent is the cell from which the search first discovered it.
    For example: parent of (2, 0) = (1, 0)
    This means the search reached (2, 0) through (1, 0). It does not mean the robot physically moved there.

    The parent record serves two purposes:
    - Prevent rediscovering cells.
    - Reconstruct the route after finding the goal.
    Mark a cell as discovered when you add it to the queue, rather than waiting until you remove it. Otherwise, several cells could enqueue the same neighbor.
    