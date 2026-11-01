import unittest

from layout_optimizer import (
    Workstation,
    optimize_layout,
    workstation_gap,
)


class TestWorkstationSpacing(unittest.TestCase):

    def test_dimensions_preserved(self):
        stations = {
            "A": Workstation("A", 0, 0, 2, 3),
            "B": Workstation("B", 10, 0, 4, 2),
        }
        result = optimize_layout(stations, {})
        self.assertEqual(result.stations["A"].width, 2)
        self.assertEqual(result.stations["A"].height, 3)
        self.assertEqual(result.stations["B"].width, 4)
        self.assertEqual(result.stations["B"].height, 2)

    def test_edge_to_edge_gap(self):
        a = Workstation("A", 0, 0, 2, 2)
        b = Workstation("B", 5, 0, 2, 2)
        self.assertEqual(workstation_gap(a, b), 3)

    def test_diagonal_gap(self):
        a = Workstation("A", 0, 0, 2, 2)
        b = Workstation("B", 5, 6, 2, 2)
        self.assertAlmostEqual(workstation_gap(a, b), 5)

    def test_rejects_negative_spacing(self):
        stations = {"A": Workstation("A", 0, 0)}
        with self.assertRaisesRegex(ValueError, "non-negative"):
            optimize_layout(stations, {}, minimum_spacing=-1)

    def test_rejects_impossible_spacing(self):
        stations = {
            "A": Workstation("A", 0, 0),
            "B": Workstation("B", 1, 0),
        }
        with self.assertRaisesRegex(ValueError, "No valid layout"):
            optimize_layout(stations, {}, minimum_spacing=5)


if __name__ == "__main__":
    unittest.main()
