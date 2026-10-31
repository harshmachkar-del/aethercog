"""AetherCog — Industrial Layout Optimization Engine."""

from dataclasses import dataclass
from itertools import permutations
from math import hypot, isfinite
from typing import Dict, Tuple, FrozenSet, Optional


@dataclass(frozen=True)
class Workstation:
    name: str
    x: float
    y: float


@dataclass(frozen=True)
class OptimizationResult:
    stations: Dict[str, Workstation]
    original_cost: float
    optimized_cost: float
    improvement_percent: float
    arrangements_evaluated: int


def distance(a: Workstation, b: Workstation) -> float:
    """Calculate straight-line distance between two workstations."""
    return hypot(a.x - b.x, a.y - b.y)


def total_transport_distance(
    stations: Dict[str, Workstation],
    material_flows: Dict[Tuple[str, str], float],
) -> float:
    """Calculate flow-weighted transportation distance."""

    total = 0.0

    for (source, destination), flow in material_flows.items():
        if source not in stations or destination not in stations:
            raise ValueError(
                "Material flow references an unknown workstation."
            )

        if not isfinite(flow) or flow < 0:
            raise ValueError(
                "Material flow must be finite and non-negative."
            )

        total += distance(
            stations[source], stations[destination]
        ) * flow

    return total


def optimize_layout(
    stations: Dict[str, Workstation],
    material_flows: Dict[Tuple[str, str], float],
    fixed_workstations: Optional[FrozenSet[str]] = None,
) -> OptimizationResult:
    """
    Find the lowest-cost assignment of workstation positions.

    Fixed workstations remain at their original coordinates.
    Other workstations may exchange positions.

    Exhaustively evaluates valid arrangements.
    Supports at most eight workstations.
    """

    if len(stations) > 8:
        raise ValueError(
            "Exhaustive optimization supports at most 8 workstations."
        )

    if len(set(stations)) != len(stations):
        raise ValueError("Workstation names must be unique.")

    for name, station in stations.items():
        if name != station.name:
            raise ValueError(
                "Dictionary keys must match workstation names."
            )

        if not isfinite(station.x) or not isfinite(station.y):
            raise ValueError("Workstation coordinates must be finite.")

    fixed = set(fixed_workstations or ())

    unknown_fixed = fixed - set(stations)

    if unknown_fixed:
        raise ValueError(
            "Fixed workstation references an unknown workstation."
        )

    names = sorted(stations)

    movable_names = [
        name for name in names if name not in fixed
    ]

    movable_positions = [
        (stations[name].x, stations[name].y)
        for name in movable_names
    ]

    original_cost = total_transport_distance(
        stations, material_flows
    )

    best_cost = float("inf")
    best_layout = None
    evaluated = 0

    for arrangement in permutations(movable_positions):
        candidate = {
            name: stations[name]
            for name in fixed
        }

        for name, position in zip(movable_names, arrangement):
            candidate[name] = Workstation(
                name, position[0], position[1]
            )

        candidate_cost = total_transport_distance(
            candidate, material_flows
        )

        evaluated += 1

        if candidate_cost < best_cost:
            best_cost = candidate_cost
            best_layout = candidate

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
        arrangements_evaluated=evaluated,
    )
