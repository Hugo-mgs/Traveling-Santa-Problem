"""
Path and Solution containers for the Traveling Santa Problem.

A Solution is a pair of disjoint paths (no shared undirected edge).
Score = max(distance(path1), distance(path2)).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Set

from .graph import Edge, Graph, make_edge


@dataclass
class Path:
    """An ordered sequence of city ids representing a tour/path."""

    cities: List[int] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------

    def total_distance(self, graph: Graph) -> float:
        if len(self.cities) < 2:
            return 0.0
        return sum(
            graph.distance(self.cities[i], self.cities[i + 1])
            for i in range(len(self.cities) - 1)
        )

    def edge_set(self) -> Set[Edge]:
        return {
            make_edge(self.cities[i], self.cities[i + 1])
            for i in range(len(self.cities) - 1)
        }

    def __len__(self) -> int:
        return len(self.cities)

    def __repr__(self) -> str:
        return f"Path(n={len(self.cities)}, cities={self.cities[:5]}{'...' if len(self.cities) > 5 else ''})"


@dataclass
class Solution:
    """
    A pair of edge-disjoint paths that together cover all cities.
    Score is defined as max(dist(path1), dist(path2)).
    """

    path1: Path
    path2: Path

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def is_valid(self, graph: Graph) -> bool:
        """Check that the two paths share no undirected edge."""
        return len(self.path1.edge_set() & self.path2.edge_set()) == 0

    def shared_edges(self) -> Set[Edge]:
        return self.path1.edge_set() & self.path2.edge_set()

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    def score(self, graph: Graph) -> float:
        """Lower is better: the larger of the two path distances."""
        return max(self.path1.total_distance(graph), self.path2.total_distance(graph))

    def distances(self, graph: Graph) -> tuple[float, float]:
        return self.path1.total_distance(graph), self.path2.total_distance(graph)

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_dict(self, graph: Graph) -> dict:
        d1, d2 = self.distances(graph)
        return {
            "score": self.score(graph),
            "path1_distance": d1,
            "path2_distance": d2,
            "path1": self.path1.cities,
            "path2": self.path2.cities,
            "valid": self.is_valid(graph),
        }

    def __repr__(self) -> str:
        return f"Solution(path1_len={len(self.path1)}, path2_len={len(self.path2)})"
