import random
from core.solution import Solution, Path

#Linear Order Crossover (LOX) for a single path, excluding the depot (first and last city).
def linear_order_crossover(parent1: list[int], parent2: list[int]) -> list[int]:
    # remove the starting node from both ends
    p1 = parent1[1:-1]
    p2 = parent2[1:-1]

    n = len(p1)

    # pick two random cut points
    i, j = sorted(random.sample(range(n), 2))

    # copy segment from parent1
    child = [None] * n
    child[i:j+1] = p1[i:j+1]

    # fill remaining positions with parent2 order
    segment = set(child[i:j+1])
    p2_order = [c for c in p2 if c not in segment]
    ptr = 0
    for k in range(n):
        if child[k] is None:
            child[k] = p2_order[ptr]
            ptr += 1

    return [0] + child + [0]

#Apply LOX to both paths and return a child solution.
def crossover(parent1: Solution, parent2: Solution) -> Solution:
    child_path1 = linear_order_crossover(parent1.path1.cities, parent2.path1.cities)
    child_path2 = linear_order_crossover(parent1.path2.cities, parent2.path2.cities)
    return Solution(Path(child_path1), Path(child_path2))

#Fix disjointness violations by reinserting one endpoint of each shared edge.
def fix_shared_edges(solution: Solution) -> Solution:
    path1 = solution.path1.cities[:]
    path2 = solution.path2.cities[:]

    shared = solution.shared_edges()
    while shared:
        edge = next(iter(shared))
        a, b = tuple(edge)

        # pick the endpoint that isn't the depot
        city = b if b != 0 else a

        # remove it from path2 and reinsert at a random position
        if city in path2[1:-1]:
            path2.remove(city)
            idx = random.randint(1, len(path2) - 1)
            path2.insert(idx, city)
        elif city in path1[1:-1]:
            path1.remove(city)
            idx = random.randint(1, len(path1) - 1)
            path1.insert(idx, city)

        solution = Solution(Path(path1), Path(path2))
        shared = solution.shared_edges()

    return solution