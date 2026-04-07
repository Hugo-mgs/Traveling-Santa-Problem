"""
Undirected graph representation for the Traveling Santa Problem.
Cities are nodes; edges are undirected and carry Euclidean distance weights.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, FrozenSet, List, Optional, Tuple


@dataclass(frozen=True)
class City:
    id: int
    x: float
    y: float

    def distance_to(self, other: "City") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)

    def __repr__(self) -> str:
        return f"City({self.id})"


# An undirected edge is represented as a frozenset of two city ids
Edge = FrozenSet[int]


def make_edge(a: int, b: int) -> Edge:
    return frozenset({a, b})


@dataclass
class Graph:
    """Weighted undirected complete graph over a set of cities."""

    cities: Dict[int, City] = field(default_factory=dict)
    _dist_cache: Dict[Tuple[int, int], float] = field(
        default_factory=dict, repr=False, compare=False
    )

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def from_csv(cls, path: str | Path) -> "Graph":
        """Load cities from a CSV file with columns: id, x, y."""
        g = cls()
        with open(path, newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                city = City(id=int(row["id"]), x=float(row["x"]), y=float(row["y"]))
                g.cities[city.id] = city
        return g

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    @property
    def city_ids(self) -> List[int]:
        return list(self.cities.keys())

    def distance(self, a: int, b: int) -> float:
        """Return cached Euclidean distance between city ids a and b."""
        key = (min(a, b), max(a, b))
        if key not in self._dist_cache:
            self._dist_cache[key] = self.cities[a].distance_to(self.cities[b])
        return self._dist_cache[key]

    def neighbors(self, city_id: int, exclude: Optional[FrozenSet[int]] = None) -> List[int]:
        """Return all city ids reachable from city_id (all others in a complete graph)."""
        return [
            cid for cid in self.cities if cid != city_id and (exclude is None or cid not in exclude)
        ]

    def nearest_neighbors(
        self,
        city_id: int,
        k: Optional[int] = None,
        exclude_edges: Optional[set] = None,
    ) -> List[int]:
        """
        Return city ids sorted by distance from city_id.
        Optionally skip cities whose edge to city_id is in exclude_edges.
        """
        exclude_edges = exclude_edges or set()
        candidates = [
            cid
            for cid in self.cities
            if cid != city_id and make_edge(city_id, cid) not in exclude_edges
        ]
        candidates.sort(key=lambda cid: self.distance(city_id, cid))
        return candidates[:k] if k is not None else candidates

    def __len__(self) -> int:
        return len(self.cities)

    def __repr__(self) -> str:
        return f"Graph(n_cities={len(self)})"
