# Traveling Santa Problem — Algorithm Comparison Framework

A clean, extensible Python framework for comparing algorithms on the **Traveling Santa Problem (disjoint two-path variant)**.

---

## Problem Definition

You are given a set of cities (id, x, y). Find **two edge-disjoint paths** that together visit all cities, minimising the score defined as:

```
score = max(distance(path₁), distance(path₂))
```

Two paths are **edge-disjoint** if no undirected edge (A↔B) appears in both.

---

## Project Structure

```
traveling_santa/
│
├── core/
│   ├── graph.py          # City, Edge, Graph — undirected weighted graph
│   └── solution.py       # Path, Solution — containers + validation + scoring
│
├── algorithms/
│   ├── base.py           # BaseAlgorithm ABC — all algorithms implement solve()
│   ├── random_baseline.py        # Random shuffle baseline
│   ├── nearest_neighbor.py       # Greedy nearest-neighbour
│   ├── greedy_edge_split.py      # Alternating greedy edge assignment
│   └── two_opt.py                # 2-Opt local search (wraps any seed algorithm)
│
├── experiments/
│   └── runner.py         # ExperimentRunner — timing, recording, CSV/JSON export
│
├── data/
│   └── generator.py      # Synthetic dataset generation (random, clustered, circle)
│
├── tests/
│   └── test_core.py      # pytest unit tests
│
├── main.py               # CLI entry point
└── requirements.txt
```

---

## Quick Start

```bash
# 1. Install (no external deps for core algorithms)
pip install pytest   # only needed for tests

# 2. Run demo with 50 synthetic cities
python -m traveling_santa.main

# 3. Run on your own dataset
python -m traveling_santa.main --csv path/to/cities.csv

# 4. Run tests
python -m pytest traveling_santa/tests/ -v
```

### CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--csv` | None | Path to cities CSV (id, x, y). If omitted, synthetic data is used. |
| `--n` | 50 | Number of synthetic cities. |
| `--seed` | 42 | Global random seed for reproducibility. |
| `--out-dir` | `results/` | Directory for CSV/JSON exports. |

---

## Dataset Format

```csv
id,x,y
0,123.45,678.90
1,234.56,789.01
...
```

Compatible with the [Kaggle Traveling Santa](https://www.kaggle.com/competitions/traveling-santa-problem) dataset format.

---

## Algorithms

| Name | Class | Description |
|------|-------|-------------|
| `Random` | `RandomAlgorithm` | Random permutation baseline |
| `NearestNeighbor` | `NearestNeighborAlgorithm` | Greedy nearest-neighbour; Path 2 avoids Path 1 edges |
| `GreedyEdgeSplit` | `GreedyEdgeSplitAlgorithm` | Alternating cheapest-edge assignment with cycle detection |
| `TwoOpt` | `TwoOptAlgorithm` | 2-Opt local search seeded by any algorithm |

---

## Adding a New Algorithm

1. Create `traveling_santa/algorithms/my_algo.py`
2. Subclass `BaseAlgorithm` and implement `solve(graph) -> Solution`:

```python
from traveling_santa.algorithms.base import BaseAlgorithm
from traveling_santa.core.graph import Graph
from traveling_santa.core.solution import Solution

class MyAlgorithm(BaseAlgorithm):
    name = "MyAlgorithm"

    def __init__(self, my_param: int = 10) -> None:
        super().__init__(my_param=my_param)
        self.my_param = my_param

    def solve(self, graph: Graph) -> Solution:
        # ... your logic here ...
        return Solution(path1=..., path2=...)
```

3. Add it to `main.py`'s `build_algorithm_suite()`.

---

## Exported Results

Every run exports to `results/<dataset_name>_results.csv` and `.json`.

### CSV columns

| Column | Description |
|--------|-------------|
| `run_id` | Unique run identifier |
| `timestamp` | UTC ISO timestamp |
| `dataset_name` | Source CSV stem name |
| `algorithm_name` | Algorithm class name |
| `algorithm_params` | JSON dict of hyperparameters |
| `execution_time_s` | Wall-clock time in seconds |
| `score` | `max(path1_distance, path2_distance)` |
| `path1_distance` | Total length of Path 1 |
| `path2_distance` | Total length of Path 2 |
| `is_valid` | True if paths are truly edge-disjoint |
| `path1` | JSON list of city ids in order |
| `path2` | JSON list of city ids in order |

---

## Running Programmatically

```python
from traveling_santa.core.graph import Graph
from traveling_santa.algorithms.two_opt import TwoOptAlgorithm
from traveling_santa.experiments.runner import ExperimentRunner

graph = Graph.from_csv("data/cities.csv")
runner = ExperimentRunner(graph, dataset_name="cities")

result = runner.run(TwoOptAlgorithm(max_iterations=100))
print(f"Score: {result.score:.2f}")

runner.export_csv("results/run.csv")
runner.export_json("results/run.json")
```
