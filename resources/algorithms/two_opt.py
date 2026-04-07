"""
2-Opt local-search improvement for the Traveling Santa Problem.

Workflow
--------
1. Generate an initial solution with a configurable seed algorithm
   (defaults to NearestNeighbor).
2. Apply 2-opt moves to Path 1 until no improving swap is found.
3. Apply 2-opt moves to Path 2, ensuring no newly introduced edge
   already exists in Path 1.

2-opt: swap edges (i, i+1) and (j, j+1) by reversing the sub-path
between i+1 and j, accepting the move only when it shortens the path
and does not produce a conflict with the other path's edge set.
"""

from __future__ import annotations

from typing import List, Optional, Set, Type

from algorithms.base import BaseAlgorithm
from algorithms.nearest_neighbor import NearestNeighborAlgorithm
from core.graph import Edge, Graph, make_edge
from core.solution import Path, Solution


class TwoOptAlgorithm(BaseAlgorithm):
    """
    Parameters
    ----------
    seed_algorithm : BaseAlgorithm instance | None
        Algorithm used to generate the initial solution.
        Defaults to NearestNeighborAlgorithm().
    max_iterations : int
        Maximum passes over the path before stopping (per path).
    random_seed : int | None
        Forwarded to the seed algorithm if it accepts one.
    """

    name = "TwoOpt"

    def __init__(
        self,
        seed_algorithm: Optional[BaseAlgorithm] = None,
        max_iterations: int = 100,
        random_seed: Optional[int] = None,
    ) -> None:
        super().__init__(
            seed_algorithm=repr(seed_algorithm or "NearestNeighbor(default)"),
            max_iterations=max_iterations,
            random_seed=random_seed,
        )
        self._seed = seed_algorithm or NearestNeighborAlgorithm(random_seed=random_seed)
        self.max_iterations = max_iterations

    # ------------------------------------------------------------------

    def solve(self, graph: Graph) -> Solution:
        solution = self._seed.solve(graph)

        p1_cities = self._two_opt(graph, solution.path1.cities, forbidden=set())
        p1 = Path(cities=p1_cities)

        p2_cities = self._two_opt(graph, solution.path2.cities, forbidden=p1.edge_set())
        p2 = Path(cities=p2_cities)

        return Solution(path1=p1, path2=p2)

    # ------------------------------------------------------------------

    def _two_opt(
        self,
        graph: Graph,
        route: List[int],
        forbidden: Set[Edge],
    ) -> List[int]:
        """Iterative 2-opt until no improving non-conflicting swap exists."""
        best = list(route)
        n = len(best)

        for _ in range(self.max_iterations):
            improved = False
            for i in range(1, n - 2):
                for j in range(i + 1, n - 1):
                    # Current edges
                    d_old = graph.distance(best[i - 1], best[i]) + graph.distance(
                        best[j], best[j + 1]
                    )
                    # Proposed edges after reversal
                    d_new = graph.distance(best[i - 1], best[j]) + graph.distance(
                        best[i], best[j + 1]
                    )

                    if d_new < d_old - 1e-10:
                        # Check that new edges don't conflict with forbidden set
                        e1 = make_edge(best[i - 1], best[j])
                        e2 = make_edge(best[i], best[j + 1])
                        if e1 not in forbidden and e2 not in forbidden:
                            best[i : j + 1] = reversed(best[i : j + 1])
                            improved = True
            if not improved:
                break

        return best
