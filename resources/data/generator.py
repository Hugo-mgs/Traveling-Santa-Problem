"""
Synthetic dataset generator for the Traveling Santa Problem.

Creates reproducible CSV files in the required format (id, x, y).
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path
from typing import Optional


def generate_random(
    n: int,
    output_path: str | Path,
    x_range: tuple[float, float] = (0.0, 1000.0),
    y_range: tuple[float, float] = (0.0, 1000.0),
    random_seed: Optional[int] = 42,
) -> Path:
    """Generate *n* cities uniformly at random."""
    rng = random.Random(random_seed)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "x", "y"])
        for i in range(n):
            writer.writerow([
                i,
                round(rng.uniform(*x_range), 4),
                round(rng.uniform(*y_range), 4),
            ])
    print(f"Generated {n}-city random dataset → {out}")
    return out


def generate_clustered(
    n: int,
    n_clusters: int,
    output_path: str | Path,
    spread: float = 60.0,
    random_seed: Optional[int] = 42,
) -> Path:
    """Generate *n* cities grouped around *n_clusters* centroids."""
    rng = random.Random(random_seed)
    centroids = [(rng.uniform(100, 900), rng.uniform(100, 900)) for _ in range(n_clusters)]
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "x", "y"])
        for i in range(n):
            cx, cy = rng.choice(centroids)
            x = cx + rng.gauss(0, spread)
            y = cy + rng.gauss(0, spread)
            writer.writerow([i, round(x, 4), round(y, 4)])
    print(f"Generated {n}-city clustered dataset ({n_clusters} clusters) → {out}")
    return out


def generate_circle(
    n: int,
    output_path: str | Path,
    radius: float = 400.0,
    center: tuple[float, float] = (500.0, 500.0),
) -> Path:
    """Place *n* cities evenly on a circle (known optimal solution exists)."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    cx, cy = center
    with open(out, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "x", "y"])
        for i in range(n):
            angle = 2 * math.pi * i / n
            writer.writerow([
                i,
                round(cx + radius * math.cos(angle), 4),
                round(cy + radius * math.sin(angle), 4),
            ])
    print(f"Generated {n}-city circle dataset → {out}")
    return out
