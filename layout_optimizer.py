"""AetherCog — Industrial Layout Optimization Engine."""

from dataclasses import dataclass
from math import hypot
from typing import Dict, Tuple


@dataclass(frozen=True)
class Workstation:
    name: str
    x: float
    y: float


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

        if flow < 0:
            raise ValueError("Material flow cannot be negative.")

        total += distance(
            stations[source],
            stations[destination]
        ) * flow

    return total
