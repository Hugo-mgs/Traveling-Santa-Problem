"""
Unit tests for the Traveling Santa core and algorithms.
Run with: python -m pytest traveling_santa/tests/ -v
"""

import pytest
import sys
import os

# Ensure package is importable when running tests directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.graph import Graph, City, make_edge
from core.solution import Path, Solution
from algorithms.random_baseline import RandomAlgorithm
from algorithms.nearest_neighbor import NearestNeighborAlgorithm
from algorithms.greedy_edge_split import GreedyEdgeSplitAlgorithm
from algorithms.two_opt import TwoOptAlgorithm


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def small_graph():
    """5-city square + center graph."""
    g = Graph()
    cities = [
        City(0, 0, 0), City(1, 100, 0), City(2, 100, 100),
        City(3, 0, 100), City(4, 50, 50),
    ]
    g.cities = {c.id: c for c in cities}
    return g


@pytest.fixture
def ten_city_graph():
    """10 cities in a grid."""
    g = Graph()
    for i in range(10):
        g.cities[i] = City(i, (i % 5) * 100.0, (i // 5) * 100.0)
    return g


# ---------------------------------------------------------------------------
# Graph tests
# ---------------------------------------------------------------------------

class TestGraph:
    def test_distance_symmetric(self, small_graph):
        assert small_graph.distance(0, 1) == small_graph.distance(1, 0)

    def test_distance_zero_self(self, small_graph):
        assert small_graph.distance(0, 0) == 0.0

    def test_nearest_neighbors_order(self, small_graph):
        nn = small_graph.nearest_neighbors(0)
        dists = [small_graph.distance(0, n) for n in nn]
        assert dists == sorted(dists)

    def test_nearest_neighbors_exclude_edge(self, small_graph):
        forbidden = {make_edge(0, 1)}
        nn = small_graph.nearest_neighbors(0, exclude_edges=forbidden)
        assert 1 not in nn


# ---------------------------------------------------------------------------
# Path / Solution tests
# ---------------------------------------------------------------------------

class TestSolution:
    def test_edge_set(self):
        p = Path(cities=[0, 1, 2, 3])
        es = p.edge_set()
        assert make_edge(0, 1) in es
        assert make_edge(1, 2) in es
        assert make_edge(0, 2) not in es

    def test_valid_disjoint(self, small_graph):
        p1 = Path(cities=[0, 1, 2])
        p2 = Path(cities=[3, 4, 2])
        sol = Solution(path1=p1, path2=p2)
        assert sol.is_valid(small_graph)

    def test_invalid_shared_edge(self, small_graph):
        p1 = Path(cities=[0, 1, 2])
        p2 = Path(cities=[2, 1, 3])  # edge 1-2 shared
        sol = Solution(path1=p1, path2=p2)
        assert not sol.is_valid(small_graph)

    def test_score_is_max(self, small_graph):
        p1 = Path(cities=[0, 1])
        p2 = Path(cities=[2, 3])
        sol = Solution(path1=p1, path2=p2)
        d1, d2 = sol.distances(small_graph)
        assert sol.score(small_graph) == max(d1, d2)


# ---------------------------------------------------------------------------
# Algorithm tests
# ---------------------------------------------------------------------------

ALGORITHMS = [
    RandomAlgorithm(random_seed=0),
    NearestNeighborAlgorithm(random_seed=0),
    GreedyEdgeSplitAlgorithm(),
    TwoOptAlgorithm(max_iterations=5, random_seed=0),
]


@pytest.mark.parametrize("algorithm", ALGORITHMS, ids=lambda a: a.name)
class TestAlgorithms:
    def test_returns_solution(self, algorithm, ten_city_graph):
        sol = algorithm.solve(ten_city_graph)
        assert isinstance(sol, Solution)

    def test_paths_non_empty(self, algorithm, ten_city_graph):
        sol = algorithm.solve(ten_city_graph)
        assert len(sol.path1) > 0
        assert len(sol.path2) > 0

    def test_solution_is_disjoint(self, algorithm, ten_city_graph):
        sol = algorithm.solve(ten_city_graph)
        assert sol.is_valid(ten_city_graph), (
            f"{algorithm.name} produced shared edges: {sol.shared_edges()}"
        )

    def test_score_positive(self, algorithm, ten_city_graph):
        sol = algorithm.solve(ten_city_graph)
        assert sol.score(ten_city_graph) > 0
