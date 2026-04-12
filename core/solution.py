from .graph import Graph, Edge, make_edge

from dataclasses import dataclass, field

@dataclass
class Path:
    """An ordered sequence of city ids representing a path"""

    cities: list[int] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Metrics
    # ------------------------------------------------------------------

    def total_distance(self, graph: Graph) -> float:
        if len(self.cities) < 2:
            return 0.0
        dist = sum(
            graph.distance(self.cities[i], self.cities[i + 1])
            for i in range(len(self.cities) - 1)
        )
        return round(dist, 2)

    def edge_set(self) -> set[Edge]:
        return {
            make_edge(self.cities[i], self.cities[i+1])
            for i in range(len(self.cities) - 1)
        }
    
    # ------------------------------------------------------------------
    
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

    def shared_edges(self) -> set[Edge]:
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
    # Saving
    # ------------------------------------------------------------------

    def to_csv(self, filename: str):
        """Save the solution to a CSV file."""
        with open(filename, "w") as f:
            f.write(",".join(map(str, self.path1.cities)) + "\n")
            f.write(",".join(map(str, self.path2.cities)) + "\n")

    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"Solution(path1_len={len(self.path1)}, path2_len={len(self.path2)})"