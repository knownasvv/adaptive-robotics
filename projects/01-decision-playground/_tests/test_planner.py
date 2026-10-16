import unittest

from engine.planner import get_neighbors, find_path


GRID = (4, 3)

class TestPlanner(unittest.TestCase):
    def test_find_path(self):
        cases = [
            {
                'start': (1, 1),
                'goal': (3, 1),
                'obstacles': {(2, 1)},
                'expected_return': [(1, 1), (1, 0), (2, 0), (3, 0), (3, 1)],
            },
            {
                'start': (1, 1),
                'goal': (1, 1),
                'obstacles': set(),
                'expected_return': [(1, 1)],
            },
            {
                'start': (1, 1),
                'goal': (3, 1),
                'obstacles': {(1, 0), (1, 2), (0, 1), (2, 1)},
                'expected_return': None
            }
        ]

        for index, case in enumerate(cases):
            start = case['start']
            goal = case['goal']
            obstacles = case['obstacles']
            expected_return = case['expected_return']
            
            with self.subTest(index=index):
                path = find_path(
                    grid=GRID,
                    obstacles=obstacles,
                    start=start,
                    goal=goal
                )
                self.assertEqual(path, expected_return)

    def test_get_neighbors(self):
        cases = [
            { # 1. Exclude an occupied neighbor
                'position': (1, 1),
                'obstacles': {(2, 1)},
                'expected_neighbors': [(1, 0), (1, 2), (0, 1)]
            }, { # 2. Exclude candidates beyond two boundaries
                'position': (0, 0),
                'obstacles': set(),
                'expected_neighbors': [(0, 1), (1, 0)]
            }, { # 3. Exclude the opposite corner
                'position': (3, 2),
                'obstacles': set(),
                'expected_neighbors': [(3, 1), (2, 2)]
            }, { # 4. A completely enclosed position
                'position': (1, 1),
                'obstacles': {(1, 0), (1, 2), (0, 1), (2, 1)},
                'expected_neighbors': []
            }
        ]

        for index, case in enumerate(cases):
            position = case['position']
            obstacles = case['obstacles']
            expected_neighbors = case['expected_neighbors']
            original_position = position
            original_obstacles = obstacles.copy()


            with self.subTest(index=index):
                neighbors = get_neighbors(
                    grid=GRID,
                    obstacles=obstacles,
                    position=position
                )

                self.assertEqual(neighbors, expected_neighbors)
                self.assertEqual(position, original_position)
                self.assertEqual(obstacles, original_obstacles)
                self.assertEqual(len(set(neighbors)), len(neighbors))


if __name__ == '__main__':
    unittest.main()