import unittest

from robot_navigation import (
    find_nearest_object, 
    Grid,
    Robot,
    ROWS,
    COLS,
    bfs_shortest_path
)

class TestRobotNavigation(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(ROWS, COLS)
        self.grid.grid = [[0] * COLS for _ in range(ROWS)]  
        self.robot = Robot(self.grid)

    def test_find_nearest_object(self):
        self.grid.grid = [[0] * COLS for _ in range(ROWS)]
        
        self.grid.grid[2][3] = 2 
        self.grid.grid[5][6] = 2 

        self.robot.row, self.robot.col = 2, 2 

        nearest = find_nearest_object(self.grid, self.robot)
        self.assertEqual(nearest, (2, 3), "Should find the nearest object at (2, 3)")

    def test_hurdle_detection(self):
        self.grid.grid[1][1] = 1  
        self.grid.grid[1][2] = 1  
        self.assertTrue(self.grid.grid[1][1] == 1, "Should detect a hurdle at (1, 1)")
        self.assertTrue(self.grid.grid[1][2] == 1, "Should detect a hurdle at (1, 2)")

    def test_environment_model_analysis(self):
        hurdles = sum(row.count(1) for row in self.grid.grid)
        objects = sum(row.count(2) for row in self.grid.grid)
        self.assertIsInstance(hurdles, int, "Hurdles count should be an integer")
        self.assertIsInstance(objects, int, "Objects count should be an integer")

    def test_robot_move(self):
        initial_position = (self.robot.row, self.robot.col)
        self.robot.move((0, 1))  
        new_position = (self.robot.row, self.robot.col)
        self.assertNotEqual(initial_position, new_position, "Robot should move to the right")

    def test_bfs_shortest_path(self):
        self.robot.row, self.robot.col = 0, 0  
        target = (4, 4)
        for i in range(5):
            self.grid.grid[i][4] = 0  
        self.grid.grid[4][4] = 0  

        path = bfs_shortest_path(self.grid, (self.robot.row, self.robot.col), target)
        self.assertGreater(len(path), 0, "Should find a path to the target")
        self.assertEqual(path[-1], target, "Path should end at the target position")

    def test_avoided_hurdles(self):
        self.grid.grid[1][1] = 1  
        self.grid.grid[1][2] = 1  
        self.grid.grid[2][1] = 1  
        
        self.robot.row, self.robot.col = 1, 0
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  
        for move in moves:
            target_row = self.robot.row + move[0]
            target_col = self.robot.col + move[1]
            
            if 0 <= target_row < self.grid.rows and 0 <= target_col < self.grid.cols:
                if self.grid.grid[target_row][target_col] == 1:
                    continue
                self.robot.move(move)
                self.assertNotEqual(self.robot.grid.grid[self.robot.row][self.robot.col], 1, 
                                    "Robot should not move onto a hurdle")

if __name__ == '__main__':
    unittest.main()
