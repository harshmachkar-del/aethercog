import unittest

from layout_optimizer import (
    FloorBounds,
    Workstation,
    optimize_layout,
)


class TestFloorBoundaries(unittest.TestCase):

    def setUp(self):
        self.stations = {
            "A": Workstation("A", 2, 2),
            "B": Workstation("B", 8, 8),
        }
        self.flows = {("A", "B"): 5}

    def test_valid_layout_inside_floor(self):
        result = optimize_layout(
            self.stations,
            self.flows,
            floor_bounds=FloorBounds(10, 10),
        )
        self.assertEqual(result.arrangements_evaluated, 2)

    def test_rejects_station_outside_floor(self):
        stations = {
            "A": Workstation("A", 12, 2),
            "B": Workstation("B", 8, 8),
        }
        with self.assertRaisesRegex(ValueError, "outside"):
            optimize_layout(
                stations, self.flows,
                floor_bounds=FloorBounds(10, 10),
            )

    def test_rejects_invalid_floor_dimensions(self):
        with self.assertRaisesRegex(ValueError, "positive"):
            optimize_layout(
                self.stations, self.flows,
                floor_bounds=FloorBounds(0, 10),
            )

    def test_fixed_station_remains_inside_floor(self):
        result = optimize_layout(
            self.stations,
            self.flows,
            fixed_workstations=frozenset({"A"}),
            floor_bounds=FloorBounds(10, 10),
        )
        self.assertEqual(result.stations["A"], self.stations["A"])


if __name__ == "__main__":
    unittest.main()
