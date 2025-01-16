import unittest
from reinforcement import *

class TestReinforcement(unittest.TestCase):
    def test_generate_room(self):
        room = generate_room(seed=42)
        for row in room:
            self.assertEqual(len(row), 5, "Each row should have 5 cells.")
        self.assertEqual(len(room), 5, "The room should have 5 rows.")

    def test_initialize_position(self):
        room = generate_room(seed=42)
        x, y = initialize_position(room)
        self.assertEqual(room[x][y], 0, "Initial position should be an empty cell.")

    def test_initialize_learned_room(self):
        learned_room = initialize_learned_room()
        self.assertEqual(len(learned_room), 5, "learned_room should have 5 rows.")
        for row in learned_room:
            self.assertEqual(len(row), 5, "Each row in learned_room should have 5 cells.")
            self.assertTrue(all(cell == 0 for cell in row), "All cells should be initialized to 0.")

    def test_train_learning_model(self):
        learned_room = train_learning_model()
        self.assertEqual(len(learned_room), 5, "learned_room should have 5 rows.")
        self.assertTrue(all(len(row) == 5 for row in learned_room), "Each row in learned_room should have 5 cells.")
        self.assertTrue(all(cell >= 0 for row in learned_room for cell in row), "All cells should have non-negative counts.")

    def test_collect_item(self):
        room = generate_room(seed=42)
        x, y = initialize_position(room)
        collect_item(room, x, y)
        self.assertEqual(room[x][y], "C", f"Cell ({x}, {y}) should be marked as collected.")

    def test_move_robot_to_cell(self):
        room = generate_room(seed=42)
        x, y = initialize_position(room)
        visited_cells = set()
        learned_room = train_learning_model()
        result = move_robot_to_cell(x, y, room, visited_cells, learned_room)
        self.assertIn((x, y), visited_cells, f"Cell ({x}, {y}) should be marked as visited.")
        self.assertIsInstance(result, bool, "move_robot_to_cell should return a boolean.")
        
    def is_object_present(self, room, r, c):
        return (r + c) % 2 == 0

    def print_room(self, room):
        for row in room:
            print(row)
        print()

    def test_update_learning_model(self):
        learned_room = [
            [10, 40, 80, 10, 70],
            [50, 60, 20, 30, 90],
            [30, 80, 50, 40, 60],
            [70, 20, 60, 40, 10],
            [90, 10, 80, 70, 50]
        ]
        room = [
            [1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0],
            [1, 1, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1]
        ]
        update_learning_model(learned_room, room)
        print("Updated learned_room:")
        self.print_room(learned_room)

if __name__ == "__main__":
    unittest.main()
