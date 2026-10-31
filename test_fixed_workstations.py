import unittest

from layout_optimizer import Workstation, optimize_layout


class TestFixedWorkstations(unittest.TestCase):

    def test_fixed_workstation_does_not_move(self):
        stations = {
            "A": Workstation("A", 0, 0),
            "B": Workstation("B", 10, 0),
            "C": Workstation("C", 20, 0),
        }

        flows = {
            ("A", "B"): 10,
            ("A", "C"): 1,
        }

        result = optimize_layout(
            stations,
            flows,
            fixed_workstations={"B"},
        )

        self.assertEqual(
            (result.stations["B"].x, result.stations["B"].y),
            (10, 0),
        )

        self.assertEqual(result.arrangements_evaluated, 2)


if __name__ == "__main__":
    unittest.main()
