import unittest

from demo import closestObjPos, detectingObjPos, pathSelection


def empty_world():
    return [[0] * 7 for _ in range(5)]


class TestObjectSearch(unittest.TestCase):
    def test_finds_every_object(self):
        world = empty_world()
        world[0][1] = 1
        world[4][6] = 1
        self.assertEqual(detectingObjPos(world), ([0, 4], [1, 6]))

    def test_picks_the_closest_object(self):
        self.assertEqual(closestObjPos([0, 4], [1, 6], 1, 1), (0, 1))

    def test_path_goes_around_a_hurdle(self):
        world = empty_world()
        world[2][3] = 9  # hurdle between the robot and the object
        world[2][5] = 1
        path, avoided = pathSelection(world, 1, 2, 2, 5)  # robot at row 2, column 1
        self.assertEqual(path[0], (2, 1))
        self.assertEqual(path[-1], (2, 5))
        self.assertNotIn((2, 3), path)
        self.assertGreater(avoided, 0)
        for (r1, c1), (r2, c2) in zip(path, path[1:]):
            self.assertEqual(abs(r1 - r2) + abs(c1 - c2), 1)  # one step at a time

    def test_returns_no_path_when_the_object_is_walled_in(self):
        world = empty_world()
        world[0][6] = 1
        world[0][5] = 9
        world[1][6] = 9
        path, _ = pathSelection(world, 0, 4, 0, 6)
        self.assertEqual(path, [])


if __name__ == "__main__":
    unittest.main()
