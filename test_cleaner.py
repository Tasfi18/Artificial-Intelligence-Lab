import random
import unittest

from cleaner import move_left, move_right, run_vacuum, suck


class TestVacuumCleaner(unittest.TestCase):
    def test_moves_stop_at_the_walls(self):
        self.assertEqual(move_right(0, 2), 1)
        self.assertEqual(move_right(1, 2), 1)
        self.assertEqual(move_left(1), 0)
        self.assertEqual(move_left(0), 0)

    def test_suck_cleans_only_dirty_tiles(self):
        tiles = [1, 0]
        self.assertEqual(suck(tiles, 0), 1)
        self.assertEqual(tiles, [0, 0])
        self.assertEqual(suck(tiles, 1), 0)

    def test_every_dirty_tile_costs_at_least_one_action(self):
        random.seed(7)
        for _ in range(50):
            _, turns, dirt = run_vacuum(4)
            self.assertGreaterEqual(turns, dirt)
            self.assertLessEqual(turns, 4 + 3)  # one suck per tile plus three moves


if __name__ == "__main__":
    unittest.main()
