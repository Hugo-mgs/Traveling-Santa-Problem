"""
Greedy Nearest-Neighbour algorithm for the Traveling Santa Problem.

Strategy
--------
1. Build Path 1 greedily: always extend to the nearest unvisited city.
2. Build Path 2 greedily: same nearest-neighbour rule, but forbidden from
   reusing any edge already in Path 1.

Both paths start from configurable (possibly random) seed cities.
"""

from __future__ import annotations

import random
from typing import List, Optional, Set

from algorithms.base import BaseAlgorithm
from core.graph import Edge, Graph, make_edge
from core.solution import Path, Solution


class NearestNeighborAlgorithm(BaseAlgorithm):
    """
    Parameters
    ----------
    seed1 : int | None
        Starting city id for Path 1.  ``None`` → random.
    seed2 : int | None
        Starting city id for Path 2.  ``None`` → random.
    random_seed : int | None
        RNG seed for reproducibility.
    """

    name = "NearestNeighbor"

    def __init__(
        self,
        seed1: Optional[int] = None,
        seed2: Optional[int] = None,
        random_seed: Optional[int] = None,
    ) -> None:
        super().__init__(seed1=seed1, seed2=seed2, random_seed=random_seed)
        self.seed1 = seed1
        self.seed2 = seed2
        self._rng = random.Random(random_seed)

    # ------------------------------------------------------------------

    def solve(self, graph: Graph) -> Solution:
        city_ids = graph.city_ids

        start1 = self.seed1 if self.seed1 is not None else self._rng.choice(city_ids)
        path1 = self._build_path(graph, start=start1, forbidden_edges=set())

        start2 = self.seed2 if self.seed2 is not None else self._rng.choice(city_ids)
        path2 = self._build_path(graph, start=start2, forbidden_edges=path1.edge_set())

        return Solution(path1=path1, path2=path2)

    # ------------------------------------------------------------------

    def _build_path(
        self,
        graph: Graph,
        start: int,
        forbidden_edges: Set[Edge],
    ) -> Path:
        """Greedy nearest-neighbour walk that avoids *forbidden_edges*."""
        visited: Set[int] = set()
        current = start
        route: List[int] = [current]
        visited.add(current)

        while len(visited) < len(graph):
            # Candidates: unvisited cities whose edge to current isn't forbidden
            candidates = [
                cid
                for cid in graph.city_ids
                if cid not in visited and make_edge(current, cid) not in forbidden_edges
            ]

            if not candidates:
                # All remaining cities are blocked by forbidden edges.
                # Fall back to nearest reachable (may revisit or skip),
                # accepting edge reuse only as a last resort.
                candidates = [cid for cid in graph.city_ids if cid not in visited]

            if not candidates:
                break  # All cities visited

            nxt = min(candidates, key=lambda cid: graph.distance(current, cid))
            route.append(nxt)
            visited.add(nxt)
            current = nxt

        return Path(cities=route)
