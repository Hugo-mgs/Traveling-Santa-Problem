"""
Random baseline algorithm for the Traveling Santa Problem.

Generates two random permutations of the city list, using the second
permutation as a fallback when an edge clash is detected.
Useful as a lower-bound baseline (expected to perform poorly).
"""

from __future__ import annotations

import random
from typing import List, Optional, Set

from algorithms.base import BaseAlgorithm
from core.graph import Edge, Graph, make_edge
from core.solution import Path, Solution


class RandomAlgorithm(BaseAlgorithm):
    """
    Parameters
    ----------
    random_seed : int | None
        RNG seed for reproducibility.
    max_attempts : int
        How many times to reshuffle Path 2 to avoid edge conflicts.
    """

    name = "Random"

    def __init__(
        self,
        random_seed: Optional[int] = None,
        max_attempts: int = 100,
    ) -> None:
        super().__init__(random_seed=random_seed, max_attempts=max_attempts)
        self._rng = random.Random(random_seed)
        self.max_attempts = max_attempts

    # ------------------------------------------------------------------

    def solve(self, graph: Graph) -> Solution:
        city_ids = graph.city_ids[:]

        # Path 1: random shuffle
        self._rng.shuffle(city_ids)
        path1 = Path(cities=list(city_ids))
        forbidden: Set[Edge] = path1.edge_set()

        # Path 2: try random shuffles until disjoint (or give up)
        path2_cities = city_ids[:]
        for _ in range(self.max_attempts):
            self._rng.shuffle(path2_cities)
            candidate = Path(cities=list(path2_cities))
            if not (candidate.edge_set() & forbidden):
                return Solution(path1=path1, path2=candidate)

        # Accept best attempt even if not fully disjoint
        return Solution(path1=path1, path2=Path(cities=list(path2_cities)))
