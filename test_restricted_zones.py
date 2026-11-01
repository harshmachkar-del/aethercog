import unittest

from layout_optimizer import (
    FloorBounds,
    RestrictedZone,
    Workstation,
    optimize_layout,
    overlaps_restricted_zone,
)


class TestRestrictedZones(unittest.TestCase):

    def test_detects_overlap(self):
        station = Workstation("A", 1, 1, 2, 2)
        zone = RestrictedZone(2, 2, 3, 3)
        self.assertTrue(overlaps_restricted_zone(station, zone))

    def test_allows_touching_boundary(self):
        station = Workstation("A", 0, 0, 2, 2)
        zone = RestrictedZone(2, 0, 2, 2)
        self.assertFalse(overlaps_restricted_zone(station, zone))

    def test_accepts_layout_away_from_zone(self):
        stations = {
            "A": Workstation("A", 0, 0),
            "B": Workstation("B", 5, 0),
        }
        zone = RestrictedZone(3, 3, 2, 2)

        result = optimize_layout(
            stations,
            {},
            floor_bounds=FloorBounds(10, 10),
            restricted_zones=(zone,),
        )

        for station in result.stations.values():
            self.assertFalse(overlaps_restricted_zone(station, zone))

    def test_rejects_layout_when_all_assignments_overlap_zone(self):
        stations = {
            "A": Workstation("A", 0, 0),
            "B": Workstation("B", 5, 0),
        }
        zone = RestrictedZone(0, 0, 2, 2)

        with self.assertRaisesRegex(ValueError, "No valid layout"):
            optimize_layout(
                stations,
                {},
                floor_bounds=FloorBounds(10, 10),
                restricted_zones=(zone,),
            )

    def test_rejects_invalid_zone(self):
        stations = {"A": Workstation("A", 1, 1)}
        with self.assertRaisesRegex(ValueError, "Restricted zone"):
            optimize_layout(
                stations,
                {},
                restricted_zones=(RestrictedZone(0, 0, -2, 2),),
            )

    def test_rejects_zone_outside_floor(self):
        stations = {"A": Workstation("A", 1, 1)}
        with self.assertRaisesRegex(ValueError, "outside"):
            optimize_layout(
                stations,
                {},
                floor_bounds=FloorBounds(10, 10),
                restricted_zones=(RestrictedZone(9, 9, 2, 2),),
            )


if __name__ == "__main__":
    unittest.main()
