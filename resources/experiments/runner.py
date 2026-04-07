"""
Experiment runner for the Traveling Santa Problem.

Records per-run metadata (dataset, algorithm parameters, timing, distances,
paths) and exports results to CSV and JSON.
"""

from __future__ import annotations

import csv
import json
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from algorithms.base import BaseAlgorithm
from core.graph import Graph
from core.solution import Solution


# ---------------------------------------------------------------------------
# Result record
# ---------------------------------------------------------------------------

@dataclass
class ExperimentResult:
    """All metadata for a single algorithm run."""

    # Identification
    run_id: str
    timestamp: str
    dataset_name: str

    # Algorithm
    algorithm_name: str
    algorithm_params: Dict[str, Any]

    # Timing
    execution_time_s: float

    # Quality
    score: float                  # max(dist1, dist2) — lower is better
    path1_distance: float
    path2_distance: float
    is_valid: bool                # True iff paths are truly edge-disjoint

    # Trajectories
    path1: List[int]
    path2: List[int]

    # ------------------------------------------------------------------

    def to_csv_row(self) -> Dict[str, Any]:
        """Flat dict suitable for a CSV row (trajectories are JSON strings)."""
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "dataset_name": self.dataset_name,
            "algorithm_name": self.algorithm_name,
            "algorithm_params": json.dumps(self.algorithm_params),
            "execution_time_s": round(self.execution_time_s, 6),
            "score": round(self.score, 4),
            "path1_distance": round(self.path1_distance, 4),
            "path2_distance": round(self.path2_distance, 4),
            "is_valid": self.is_valid,
            "path1": json.dumps(self.path1),
            "path2": json.dumps(self.path2),
        }

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

class ExperimentRunner:
    """
    Run one or more algorithms against a graph and collect results.

    Usage
    -----
    runner = ExperimentRunner(graph, dataset_name="santa_2024")
    runner.run(NearestNeighborAlgorithm(seed1=0))
    runner.run(TwoOptAlgorithm())
    runner.export_csv("results/my_run.csv")
    runner.export_json("results/my_run.json")
    """

    def __init__(self, graph: Graph, dataset_name: str = "unknown") -> None:
        self.graph = graph
        self.dataset_name = dataset_name
        self.results: List[ExperimentResult] = []

    # ------------------------------------------------------------------
    # Running
    # ------------------------------------------------------------------

    def run(self, algorithm: BaseAlgorithm, verbose: bool = True) -> ExperimentResult:
        """Execute *algorithm* and store the result."""
        run_id = f"{algorithm.name}_{datetime.utcnow().strftime('%Y%m%dT%H%M%S%f')}"

        if verbose:
            print(f"[{self.dataset_name}] Running {algorithm} …", end=" ", flush=True)

        t0 = time.perf_counter()
        solution: Solution = algorithm.solve(self.graph)
        elapsed = time.perf_counter() - t0

        d1, d2 = solution.distances(self.graph)
        result = ExperimentResult(
            run_id=run_id,
            timestamp=datetime.utcnow().isoformat(),
            dataset_name=self.dataset_name,
            algorithm_name=algorithm.name,
            algorithm_params=algorithm.params,
            execution_time_s=elapsed,
            score=solution.score(self.graph),
            path1_distance=d1,
            path2_distance=d2,
            is_valid=solution.is_valid(self.graph),
            path1=solution.path1.cities,
            path2=solution.path2.cities,
        )
        self.results.append(result)

        if verbose:
            print(
                f"score={result.score:.2f}  "
                f"(d1={result.path1_distance:.2f}, d2={result.path2_distance:.2f})  "
                f"valid={result.is_valid}  "
                f"time={result.execution_time_s:.3f}s"
            )
        return result

    def run_all(
        self, algorithms: List[BaseAlgorithm], verbose: bool = True
    ) -> List[ExperimentResult]:
        return [self.run(alg, verbose=verbose) for alg in algorithms]

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export_csv(self, path: str | Path) -> Path:
        """Write all results to a CSV file."""
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        rows = [r.to_csv_row() for r in self.results]
        if not rows:
            print("No results to export.")
            return out
        with open(out, "w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print(f"CSV exported → {out}")
        return out

    def export_json(self, path: str | Path) -> Path:
        """Write all results to a JSON file."""
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w") as fh:
            json.dump([r.to_dict() for r in self.results], fh, indent=2)
        print(f"JSON exported → {out}")
        return out

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def summary(self) -> None:
        """Print a ranked summary table."""
        if not self.results:
            print("No results yet.")
            return
        sorted_results = sorted(self.results, key=lambda r: r.score)
        header = f"{'Rank':<5} {'Algorithm':<22} {'Score':>12} {'D1':>12} {'D2':>12} {'Time(s)':>10} {'Valid':<6}"
        print("\n" + "=" * len(header))
        print(header)
        print("=" * len(header))
        for rank, r in enumerate(sorted_results, 1):
            print(
                f"{rank:<5} {r.algorithm_name:<22} {r.score:>12.2f} "
                f"{r.path1_distance:>12.2f} {r.path2_distance:>12.2f} "
                f"{r.execution_time_s:>10.3f} {'✓' if r.is_valid else '✗':<6}"
            )
        print("=" * len(header))
