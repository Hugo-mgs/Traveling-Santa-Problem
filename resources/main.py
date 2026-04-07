"""
Traveling Santa Problem — main comparison script.

Usage
-----
    python -m traveling_santa.main                        # synthetic demo
    python -m traveling_santa.main --csv data/cities.csv  # real dataset
    python -m traveling_santa.main --help
"""

from __future__ import annotations

import argparse
from pathlib import Path

from algorithms.greedy_edge_split import GreedyEdgeSplitAlgorithm
from algorithms.nearest_neighbor import NearestNeighborAlgorithm
from algorithms.random_baseline import RandomAlgorithm
from algorithms.two_opt import TwoOptAlgorithm
from core.graph import Graph
from data.generator import generate_clustered, generate_random
from experiments.runner import ExperimentRunner


def build_algorithm_suite(random_seed: int = 42):
    """Return the full list of algorithms to benchmark."""
    return [
        RandomAlgorithm(random_seed=random_seed),
        NearestNeighborAlgorithm(random_seed=random_seed),
        NearestNeighborAlgorithm(seed1=0, seed2=1, random_seed=random_seed),
        GreedyEdgeSplitAlgorithm(max_degree=2),
        TwoOptAlgorithm(
            seed_algorithm=NearestNeighborAlgorithm(random_seed=random_seed),
            max_iterations=50,
            random_seed=random_seed,
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Traveling Santa — algorithm comparison")
    parser.add_argument("--csv", type=str, default=None, help="Path to cities CSV (id,x,y)")
    parser.add_argument("--n", type=int, default=50, help="Cities for synthetic demo (default 50)")
    parser.add_argument("--seed", type=int, default=42, help="Global random seed")
    parser.add_argument("--out-dir", type=str, default="results", help="Output directory")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)

    # ------------------------------------------------------------------ #
    # Load or generate dataset
    # ------------------------------------------------------------------ #
    if args.csv:
        csv_path = Path(args.csv)
        dataset_name = csv_path.stem
    else:
        csv_path = out_dir / "demo_data" / f"random_{args.n}.csv"
        generate_random(n=args.n, output_path=csv_path, random_seed=args.seed)
        dataset_name = f"random_{args.n}"

    print(f"\nLoading dataset: {csv_path}")
    graph = Graph.from_csv(csv_path)
    print(f"Graph: {graph}\n")

    # ------------------------------------------------------------------ #
    # Run experiments
    # ------------------------------------------------------------------ #
    runner = ExperimentRunner(graph, dataset_name=dataset_name)
    algorithms = build_algorithm_suite(random_seed=args.seed)
    runner.run_all(algorithms)

    # ------------------------------------------------------------------ #
    # Summary + export
    # ------------------------------------------------------------------ #
    runner.summary()

    results_csv = out_dir / f"{dataset_name}_results.csv"
    results_json = out_dir / f"{dataset_name}_results.json"
    runner.export_csv(results_csv)
    runner.export_json(results_json)


if __name__ == "__main__":
    main()











