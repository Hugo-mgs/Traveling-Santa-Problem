import random
import math
from core.solution import Solution, Path
from core.graph import Graph
from algorithms.two_opt import two_opt_solution


# --------------------------------------------------
# Perturbation (reuse from k-opt idea)
# --------------------------------------------------
def perturb_path(path: Path, k: int = 2) -> Path:
    cities = path.cities[:]
    n = len(cities)

    for _ in range(k):
        i, j = sorted(random.sample(range(1, n - 1), 2))
        cities[i:j] = reversed(cities[i:j])

    return Path(cities)


def perturb_solution_valid(solution: Solution, graph: Graph, k: int = 2, max_attempts: int = 10):
    for _ in range(max_attempts):
        new_path1 = perturb_path(solution.path1, k)
        new_path2 = perturb_path(solution.path2, k)

        candidate = Solution(new_path1, new_path2)

        if candidate.is_valid(graph):
            return candidate

    return None


# --------------------------------------------------
# Simulated Annealing
# --------------------------------------------------
def simulated_annealing(
    solution: Solution,
    graph: Graph,
    initial_temp: float = 1000,
    cooling_rate: float = 0.995,
    iterations: int = 1000,
    k: int = 2
) -> Solution:

    current = solution
    current_score = current.score(graph)

    best = current
    best_score = current_score

    T = initial_temp

    for _ in range(iterations):

        # generate neighbor
        candidate = perturb_solution_valid(current, graph, k)

        if candidate is None:
            continue

        # local improvement 
        candidate = two_opt_solution(candidate, graph)
        candidate_score = candidate.score(graph)

        delta = candidate_score - current_score

        # accept if better OR with probability
        if delta < 0 or random.random() < math.exp(-delta / T):
            current = candidate
            current_score = candidate_score

            if current_score < best_score:
                best = current
                best_score = current_score

        # cool down
        T *= cooling_rate

        # optional early stop
        if T < 1e-3:
            break

    return best