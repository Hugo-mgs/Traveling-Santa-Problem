"""
Abstract base class that all Traveling Santa algorithms must implement.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from core.graph import Graph
from core.solution import Solution


class BaseAlgorithm(ABC):
    """
    All algorithms inherit from this class.

    Subclasses must implement `solve(graph) -> Solution`.
    They may expose hyperparameters as constructor arguments and should
    store them in `self.params` for result tracking.
    """

    #: Human-readable name shown in reports / exports
    name: str = "BaseAlgorithm"

    def __init__(self, **params: Any) -> None:
        self.params: Dict[str, Any] = params

    @abstractmethod
    def solve(self, graph: Graph) -> Solution:
        """
        Run the algorithm on *graph* and return a Solution.

        The returned Solution must satisfy:
          - Both paths together visit all cities (coverage policy is
            algorithm-specific: Hamiltonian split, repeated-visit, etc.)
          - No undirected edge appears in both paths (disjointness)
        """

    def __repr__(self) -> str:
        param_str = ", ".join(f"{k}={v}" for k, v in self.params.items())
        return f"{self.name}({param_str})"
