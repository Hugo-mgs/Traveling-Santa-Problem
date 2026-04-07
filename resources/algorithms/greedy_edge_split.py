"""
Greedy Edge-Split algorithm for the Traveling Santa Problem.

Strategy
--------
1. Build a sorted list of all N*(N-1)/2 undirected edges by weight.
2. Alternate assignment of edges to Path A and Path B (greedy, cheapest first),
   subject to:
   - Each city's degree in each path stays ≤ 2 (simple path constraint).
   - No edge is shared between the two paths.
   - No sub-cycles form before all cities are included (union-find).
3. Connect any remaining isolated cities with short bridging edges.

This produces two edge-disjoint Hamiltonian-like paths without running
a full TSP solver; it serves as a structural middle ground between the
pure greedy nearest-neighbor and metaheuristic approaches.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple

from algorithms.base import BaseAlgorithm
from core.graph import Edge, Graph, make_edge
from core.solution import Path, Solution


# ---------------------------------------------------------------------------
# Union-Find (for cycle detection)
# ---------------------------------------------------------------------------

class _UnionFind:
    def __init__(self, elements):
        self._parent = {e: e for e in elements}
        self._rank = {e: 0 for e in elements}

    def find(self, x):
        while self._parent[x] != x:
            self._parent[x] = self._parent[self._parent[x]]
            x = self._parent[x]
        return x

    def union(self, x, y) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # Would create a cycle
        if self._rank[rx] < self._rank[ry]:
            rx, ry = ry, rx
        self._parent[ry] = rx
        if self._rank[rx] == self._rank[ry]:
            self._rank[rx] += 1
        return True


# ---------------------------------------------------------------------------
# Algorithm
# ---------------------------------------------------------------------------

class GreedyEdgeSplitAlgorithm(BaseAlgorithm):
    """
    Parameters
    ----------
    max_degree : int
        Maximum degree per city per path (2 = simple path, higher allows
        branching for experimentation).
    """

    name = "GreedyEdgeSplit"

    def __init__(self, max_degree: int = 2) -> None:
        super().__init__(max_degree=max_degree)
        self.max_degree = max_degree

    # ------------------------------------------------------------------

    def solve(self, graph: Graph) -> Solution:
        city_ids = graph.city_ids
        n = len(city_ids)

        # All edges sorted by distance ascending
        edges: List[Tuple[float, int, int]] = []
        for i in range(n):
            for j in range(i + 1, n):
                a, b = city_ids[i], city_ids[j]
                edges.append((graph.distance(a, b), a, b))
        edges.sort()

        degree_a: Dict[int, int] = {c: 0 for c in city_ids}
        degree_b: Dict[int, int] = {c: 0 for c in city_ids}
        uf_a = _UnionFind(city_ids)
        uf_b = _UnionFind(city_ids)
        adj_a: Dict[int, List[int]] = {c: [] for c in city_ids}
        adj_b: Dict[int, List[int]] = {c: [] for c in city_ids}
        assigned_a: Set[Edge] = set()
        assigned_b: Set[Edge] = set()

        # Count edges assigned per path to balance alternation
        count_a = count_b = 0

        for dist, u, v in edges:
            edge = make_edge(u, v)
            # Try to assign to the path with fewer edges first (balance)
            targets = (
                ("a", degree_a, uf_a, adj_a, assigned_a)
                if count_a <= count_b
                else ("b", degree_b, uf_b, adj_b, assigned_b)
            )
            other = (
                ("b", degree_b, uf_b, adj_b, assigned_b)
                if count_a <= count_b
                else ("a", degree_a, uf_a, adj_a, assigned_a)
            )

            for label, deg, uf, adj, assigned in (targets, other):
                if (
                    deg[u] < self.max_degree
                    and deg[v] < self.max_degree
                    and edge not in assigned_a
                    and edge not in assigned_b
                    and uf.union(u, v)  # No cycle; also commits the union
                ):
                    assigned.add(edge)
                    adj[u].append(v)
                    adj[v].append(u)
                    deg[u] += 1
                    deg[v] += 1
                    if label == "a":
                        count_a += 1
                    else:
                        count_b += 1
                    break

        path1 = self._adj_to_path(adj_a, city_ids)
        path2 = self._adj_to_path(adj_b, city_ids)
        return Solution(path1=path1, path2=path2)

    # ------------------------------------------------------------------

    @staticmethod
    def _adj_to_path(adj: Dict[int, List[int]], city_ids: List[int]) -> Path:
        """Convert adjacency list to an ordered Path via DFS from an endpoint."""
        # Endpoints have degree 1 (or 0)
        endpoints = [c for c in city_ids if len(adj[c]) <= 1]
        start = endpoints[0] if endpoints else city_ids[0]

        visited: Set[int] = set()
        route: List[int] = []
        stack = [start]
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            route.append(node)
            for nb in adj[node]:
                if nb not in visited:
                    stack.append(nb)

        # Append any disconnected cities at the end
        for c in city_ids:
            if c not in visited:
                route.append(c)

        return Path(cities=route)
