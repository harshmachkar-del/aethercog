import unittest

from layout_optimizer import (
    Workstation,
    distance,
    total_transport_distance,
)


class TestLayoutOptimizer(unittest.TestCase):

    def setUp(self):
        self.stations = {
            "A": Workstation("A", 0, 0),
            "B": Workstation("B", 3, 4),
            "C": Workstation("C", 6, 8),
        }

    def test_distance(self):
        self.assertEqual(
            distance(self.stations["A"], self.stations["B"]),
            5.0,
        )

    def test_total_transport_distance(self):
        flows = {
            ("A", "B"): 10,
            ("B", "C"): 5,
        }

        self.assertEqual(
            total_transport_distance(self.stations, flows),
            75.0,
        )

    def test_unknown_workstation(self):
        flows = {("A", "D"): 10}

        with self.assertRaises(ValueError):
            total_transport_distance(self.stations, flows)

    def test_negative_flow(self):
        flows = {("A", "B"): -5}

        with self.assertRaises(ValueError):
            total_transport_distance(self.stations, flows)


if __name__ == "__main__":
    unittest.main()
