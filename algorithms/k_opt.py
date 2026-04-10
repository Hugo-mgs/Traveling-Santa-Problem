import random
from core.solution import Solution, Path
from core.graph import Graph
from algorithms.two_opt import two_opt_solution


# --------------------------------------------------
# Perturbation (simulates k-opt move)
# --------------------------------------------------
def perturb_path(path: Path, k: int = 3) -> Path:
    """
    Apply k random segment reversals (approximate k-opt move)
    """
    cities = path.cities[:]
    n = len(cities)

    for _ in range(k):
        i, j = sorted(random.sample(range(1, n - 1), 2))
        cities[i:j] = reversed(cities[i:j])

    return Path(cities)


# ==================================================
# Constraint-aware perturbation (valid solutions)
# ==================================================
def perturb_solution_valid(
    solution: Solution,
    graph: Graph,
    k: int = 3,
    max_attempts: int = 10
) -> Solution | None:
    """
    Try to generate a VALID perturbed solution.
    Avoids wasting iterations on invalid edge overlaps.
    """

    for _ in range(max_attempts):
        new_path1 = perturb_path(solution.path1, k)
        new_path2 = perturb_path(solution.path2, k)

        candidate = Solution(new_path1, new_path2)

        # Only accept valid (edge-disjoint) solutions
        if candidate.is_valid(graph):
            return candidate

    # failed to find valid perturbation
    return None


# --------------------------------------------------
# K-opt via Iterated Local Search (ILS)
# --------------------------------------------------
def k_opt(
    solution: Solution,
    graph: Graph,
    iterations: int = 50,
    k: int = 3
) -> Solution:
    """
    Iterated Local Search using 2-opt as local optimizer
    and k-opt style perturbations.
    """

    best = solution
    best_score = best.score(graph)

    for _ in range(iterations):
        # 1. Perturb (escape local minimum)
        candidate = perturb_solution_valid(best, graph, k)

        # 2. Skip if no valid perturbation found
        if candidate is None:
            continue

        # 3. Local search (2-opt)
        candidate = two_opt_solution(candidate, graph)
        candidate_score = candidate.score(graph)

        # 4. Accept if better
        if candidate_score < best_score:
            best = candidate
            best_score = candidate_score

    return best