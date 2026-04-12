import random
from core.graph import Graph
from core.solution import Solution, Path
from algorithms.nearest_neighbour import nearest_neighbour
from algorithms.two_opt import two_opt_solution

# Random restart hill climbing using 2-opt as the local search
def generate_neighbours(solution: Solution) -> Solution:
    path1 = solution.path1.cities[:]
    path2 = solution.path2.cities[:]
    n = max(3, len(path1) // 5)
    for _ in range(n):
        i, j = random.sample(range(1, len(path1) - 1), 2)
        path1[i], path1[j] = path1[j], path1[i]
        i, j = random.sample(range(1, len(path2) - 1), 2)
        path2[i], path2[j] = path2[j], path2[i]
    return Solution(Path(path1), Path(path2))

def hill_climbing(graph: Graph, n_restarts: int = 50) -> Solution:
    best = two_opt_solution(nearest_neighbour(graph), graph)
    for _ in range(n_restarts - 1):
        candidate = two_opt_solution(generate_neighbours(best), graph)
        if candidate.score(graph) < best.score(graph):
            best = candidate
    return best