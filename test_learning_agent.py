import unittest
import numpy as np
from tkinter import Tk
from matplotlib import pyplot as plt

class TestGridAgent(unittest.TestCase):
    
    def setUp(self):
        self.num_grids = 50
        self.grid_size = 6
        self.probability_threshold = 0.3

    def test_grid_generation(self):
        grids = [np.random.choice([0, 1], size=(self.grid_size, self.grid_size), p=[0.6, 0.4]) for _ in range(self.num_grids)]
        for grid in grids:
            self.assertEqual(grid.shape, (self.grid_size, self.grid_size))
        self.assertTrue(0 <= self.probability_threshold <= 1)

    def test_probability_grid(self):
        grids = [np.random.choice([0, 1], size=(self.grid_size, self.grid_size), p=[0.6, 0.4]) for _ in range(self.num_grids)]
        probability_grid = np.zeros((self.grid_size, self.grid_size))
        
        for grid in grids:
            probability_grid += grid
        probability_grid /= self.num_grids
        self.assertEqual(probability_grid.shape, (self.grid_size, self.grid_size))  
        self.assertTrue(np.all((0 <= probability_grid) & (probability_grid <= 1)))

    def test_agent_initialization(self):
        probability_grid = np.random.rand(self.grid_size, self.grid_size)
        max_prob_position = np.unravel_index(np.argmax(probability_grid), probability_grid.shape)
        self.assertTrue(0 <= max_prob_position[0] < self.grid_size)
        self.assertTrue(0 <= max_prob_position[1] < self.grid_size)

    def test_path_traversal(self):
        probability_grid = np.random.rand(self.grid_size, self.grid_size)
        visited = np.zeros_like(probability_grid, dtype=bool)
        path = []
        while not np.all(visited):
            unvisited_indices = np.argwhere(~visited)
            next_pos = unvisited_indices[np.argmax(probability_grid[tuple(unvisited_indices.T)])]
            visited[tuple(next_pos)] = True
            path.append(tuple(next_pos))
        self.assertEqual(len(path), self.grid_size * self.grid_size)
        self.assertTrue(np.all(visited))

    def test_visualization_initialization(self):
        fig, ax = plt.subplots(figsize=(6, 6))
        probability_grid = np.random.rand(self.grid_size, self.grid_size)
        ax.imshow(probability_grid, cmap='plasma', interpolation='none', alpha=0.9)
        ax.set_xticks(np.arange(self.grid_size))
        ax.set_yticks(np.arange(self.grid_size))
        self.assertEqual(ax.images[0].get_array().shape, probability_grid.shape)
        self.assertEqual(len(ax.get_xticks()), self.grid_size)
        self.assertEqual(len(ax.get_yticks()), self.grid_size)


if __name__ == "__main__":
    unittest.main()
