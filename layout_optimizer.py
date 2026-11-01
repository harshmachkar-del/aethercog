
from dataclasses import dataclass
from itertools import permutations
from math import hypot, isfinite
from typing import Dict, FrozenSet, Optional, Tuple


@dataclass(frozen=True)
class Workstation:
    name: str
    x: float
    y: float
    width: float = 1.0
    height: float = 1.0


@dataclass(frozen=True)
class FloorBounds:
    width: float
    height: float


@dataclass(frozen=True)
class RestrictedZone:
    x: float
    y: float
    width: float
    height: float


@dataclass(frozen=True)
class OptimizationResult:
    stations: Dict[str, Workstation]
    original_cost: float
    optimized_cost: float
    improvement_percent: float
    arrangements_evaluated: int


def distance(a: Workstation, b: Workstation) -> float:
    """Return Euclidean distance between workstation origins."""
    return hypot(a.x - b.x, a.y - b.y)


def total_transport_distance(
    stations: Dict[str, Workstation],
    material_flows: Dict[Tuple[str, str], float],
) -> float:
    """Calculate flow-weighted transport distance."""
    total = 0.0

    for (source, destination), flow in material_flows.items():
        if source not in stations or destination not in stations:
            raise ValueError("Material flow references an unknown workstation.")

        if not isfinite(flow) or flow < 0:
            raise ValueError("Material flow must be finite and non-negative.")

        total += flow * distance(
            stations[source],
            stations[destination],
        )

    return total


def overlaps_restricted_zone(
    station: Workstation,
    zone: RestrictedZone,
) -> bool:
    """Return True when workstation footprint overlaps a restricted zone."""
    return (
        station.x < zone.x + zone.width
        and station.x + station.width > zone.x
        and station.y < zone.y + zone.height
        and station.y + station.height > zone.y
    )


def workstation_gap(a: Workstation, b: Workstation) -> float:
    """Return the shortest distance between two rectangular footprints."""
    dx = max(
        0.0,
        a.x - (b.x + b.width),
        b.x - (a.x + a.width),
    )
    dy = max(
        0.0,
        a.y - (b.y + b.height),
        b.y - (a.y + a.height),
    )

    return hypot(dx, dy)


def has_sufficient_spacing(
    stations: Dict[str, Workstation],
    minimum_spacing: float,
) -> bool:
    """Check spacing between every pair of workstation footprints."""
    names = sorted(stations)

    for index, name in enumerate(names):
        for other_name in names[index + 1:]:
            if workstation_gap(
                stations[name],
                stations[other_name],
            ) < minimum_spacing:
                return False

    return True


def optimize_layout(
    stations: Dict[str, Workstation],
    material_flows: Dict[Tuple[str, str], float],
    fixed_workstations: Optional[FrozenSet[str]] = None,
    floor_bounds: Optional[FloorBounds] = None,
    minimum_spacing: float = 0.0,
    restricted_zones: Optional[Tuple[RestrictedZone, ...]] = None,
) -> OptimizationResult:
    """
    Find the lowest-cost valid assignment of existing workstation positions.

    The optimizer permutes existing coordinates. It does not generate
    new workstation positions.
    """

    if len(stations) > 8:
        raise ValueError("Optimizer supports a maximum of 8 workstations.")

    for name, station in stations.items():
        if name != station.name:
            raise ValueError("Workstation key must match workstation name.")

        if not isfinite(station.x) or not isfinite(station.y):
            raise ValueError("Workstation coordinates must be finite.")

        if (
            not isfinite(station.width)
            or not isfinite(station.height)
            or station.width <= 0
            or station.height <= 0
        ):
            raise ValueError(
                "Workstation dimensions must be finite and positive."
            )

    if floor_bounds is not None:
        if (
            not isfinite(floor_bounds.width)
            or not isfinite(floor_bounds.height)
            or floor_bounds.width <= 0
            or floor_bounds.height <= 0
        ):
            raise ValueError(
                "Floor dimensions must be finite and positive."
            )

        for station in stations.values():
            if not (
                0 <= station.x
                and 0 <= station.y
                and station.x + station.width <= floor_bounds.width
                and station.y + station.height <= floor_bounds.height
            ):
                raise ValueError(
                    "Workstation lies outside factory floor boundaries."
                )

    if not isfinite(minimum_spacing) or minimum_spacing < 0:
        raise ValueError(
            "Minimum spacing must be finite and non-negative."
        )

    zones = tuple(restricted_zones or ())

    for zone in zones:
        if (
            not isfinite(zone.x)
            or not isfinite(zone.y)
            or not isfinite(zone.width)
            or not isfinite(zone.height)
            or zone.x < 0
            or zone.y < 0
            or zone.width <= 0
            or zone.height <= 0
        ):
            raise ValueError(
                "Restricted zone dimensions and coordinates must be valid."
            )

        if floor_bounds is not None and (
            zone.x + zone.width > floor_bounds.width
            or zone.y + zone.height > floor_bounds.height
        ):
            raise ValueError(
                "Restricted zone lies outside factory floor boundaries."
            )

    fixed = set(fixed_workstations or ())

    unknown_fixed = fixed - set(stations)

    if unknown_fixed:
        raise ValueError(
            f"Unknown fixed workstations: {sorted(unknown_fixed)}"
        )

    original_cost = total_transport_distance(
        stations,
        material_flows,
    )

    names = sorted(stations)

    movable_names = [
        name for name in names if name not in fixed
    ]

    movable_positions = [
        (stations[name].x, stations[name].y)
        for name in movable_names
    ]

    best_cost = float("inf")
    best_layout = None
    arrangements_evaluated = 0

    for arrangement in permutations(movable_positions):
        candidate = {
            name: stations[name]
            for name in fixed
        }

        for name, position in zip(
            movable_names,
            arrangement,
        ):
            original = stations[name]

            candidate[name] = Workstation(
                name,
                position[0],
                position[1],
                original.width,
                original.height,
            )

        if floor_bounds is not None:
            if any(
                station.x < 0
                or station.y < 0
                or station.x + station.width > floor_bounds.width
                or station.y + station.height > floor_bounds.height
                for station in candidate.values()
            ):
                continue

        if not has_sufficient_spacing(
            candidate,
            minimum_spacing,
        ):
            continue

        if any(
            overlaps_restricted_zone(station, zone)
            for station in candidate.values()
            for zone in zones
        ):
            continue

        candidate_cost = total_transport_distance(
            candidate,
            material_flows,
        )

        arrangements_evaluated += 1

        if candidate_cost < best_cost:
            best_cost = candidate_cost
            best_layout = candidate

    if best_layout is None:
        raise ValueError(
            "No valid layout satisfies the floor, spacing, "
            "and restricted-zone constraints."
        )

    improvement = (
        ((original_cost - best_cost) / original_cost) * 100
        if original_cost > 0
        else 0.0
    )

    return OptimizationResult(
        stations=best_layout,
        original_cost=original_cost,
        optimized_cost=best_cost,
        improvement_percent=improvement,
        arrangements_evaluated=arrangements_evaluated,
    )
