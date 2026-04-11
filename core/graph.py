from dataclasses import dataclass, field
import math
import pandas as pd
from typing import FrozenSet, Dict, List, Tuple, Optional

@dataclass(frozen=True)
class City:
    id: int
    x: float
    y: float

    def distance_to(self, other: "City") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)
    
    def __repr__(self) -> str:
        return f"City({self.id}) - ({self.x},{self.y})"

# An undirected edge is represented as a frozenset of two city ids
Edge = FrozenSet[int]

def make_edge(a: int, b: int) -> Edge:
    return frozenset({a, b})

@dataclass
class Graph:
    """Weighted undirected complete graph over a set of cities."""

    cities: Dict[int, City] = field(default_factory=dict)

    """Caches previously calculated distances to be accessed again."""
    _dist_cache: Dict[Tuple[int, int], float] = field(
        default_factory=dict, repr=False, compare=False
    )

    # ------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------

    @classmethod
    def from_csv(cls, path: str):
        """Load cities from a CSV file with columns: id, x, y."""
        g = cls()
        df = pd.read_csv(path)
        g.cities = {
            row.id: City(id=row.id, x=row.x, y=row.y) for row in df.itertuples()
        }
        return g
    
    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    @property
    def city_ids(self) -> List[int]:
        return list(self.cities.keys())
    
    def distance(self, a: int, b: int) -> float:
        """
        Return cached Euclidean distance between city ids a and b.
        Keys are in the format (min,max) for standerdization purposes.
        """
        key = (min(a, b), max(a, b))
        if key not in self._dist_cache:
            self._dist_cache[key] = self.cities[a].distance_to(self.cities[b])
        return self._dist_cache[key]
    
    def neighbors(self, city_id: int, exclude: Optional[FrozenSet[int]] = None) -> List[int]:
        """Return all city ids reachable from city_id (all others in a complete graph)."""
        return [
            c_id for c_id in self.cities if c_id != city_id and (exclude is None or c_id not in exclude)
        ]
    
    def nearest_neighbours(self, city_id: int, k: Optional[int] = None, exclude_edges: Optional[set] = set()) -> List[int]:
        """
        Return city ids sorted by distance from city_id in ascending order.
        Optionally skip cities whose edge to city_id is in exclude_edges.
        Optionally limit the number of cities returned (k).
        """
        candidates = [
            c_id for c_id in self.cities
            if c_id != city_id and make_edge(city_id, c_id) not in exclude_edges
        ]
        candidates.sort(key=lambda c_id: self.distance(city_id, c_id))
        return candidates[:k] if k is not None else candidates
    
    def compute_candidate_lists(self, k: int = 20):
        """
        Precompute k nearest neighbors for each city.
        Critical for scaling 2-opt to large instances.
        """
        self.candidate_lists = {
            city: self.nearest_neighbours(city, k=k)
            for city in self.city_ids
        }
    
    # ------------------------------------------------------------------
        
    def __len__(self) -> int:
        return len(self.cities)

    def __repr__(self) -> str:
        return f"Graph(n_cities={len(self)})"