import unittest

from layout_optimizer import (
    Workstation,
    distance,
    total_transport_distance,
    optimize_layout,
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
        with self.assertRaises(ValueError):
            total_transport_distance(
                self.stations, {("A", "D"): 10}
            )

    def test_negative_flow(self):
        with self.assertRaises(ValueError):
            total_transport_distance(
                self.stations, {("A", "B"): -5}
            )

    def test_optimizer_finds_better_layout(self):
        stations = {
            "A": Workstation("A", 0, 0),
            "B": Workstation("B", 10, 0),
            "C": Workstation("C", 20, 0),
        }
        flows = {
            ("A", "B"): 10,
            ("A", "C"): 1,
        }

        result = optimize_layout(stations, flows)

        self.assertEqual(result.original_cost, 120.0)
        self.assertEqual(result.optimized_cost, 110.0)
        self.assertAlmostEqual(
            result.improvement_percent, 8.3333333333
        )
        self.assertEqual(result.arrangements_evaluated, 6)

    def test_optimizer_never_worsens_layout(self):
        flows = {
            ("A", "B"): 10,
            ("B", "C"): 5,
        }
        result = optimize_layout(self.stations, flows)

        self.assertLessEqual(
            result.optimized_cost, result.original_cost
        )

    def test_optimizer_rejects_more_than_eight_workstations(self):
        stations = {
            str(i): Workstation(str(i), i, 0)
            for i in range(9)
        }

        with self.assertRaises(ValueError):
            optimize_layout(stations, {})

    def test_optimizer_rejects_non_finite_flow(self):
        with self.assertRaises(ValueError):
            optimize_layout(
                self.stations,
                {("A", "B"): float("inf")},
            )


if __name__ == "__main__":
    unittest.main()
