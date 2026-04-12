from core.solution import Solution, Path
from core.graph import Graph


# --------------------------------------------------
# 2-opt for a single path (with pruning + candidates)
# --------------------------------------------------
def two_opt_path(path: Path, graph: Graph, forbidden_edges: set) -> Path:
    best = path.cities[:]

    # position map (avoids O(n) index lookups)
    pos = {city: i for i, city in enumerate(best)}

    improved = True
    while improved:
        improved = False

        for i in range(1, len(best) - 2):
            a = best[i - 1]
            b = best[i]

            # Only check candidate neighbors instead of all j
            for c in graph.candidate_lists[a]:
                j = pos[c]

                if j <= i or j >= len(best) - 1:
                    continue

                d = best[j + 1]

                #  Check edge-disjoint constraint BEFORE computing distances
                edge_ac = frozenset({a, c})
                edge_bd = frozenset({b, d})

                if edge_ac in forbidden_edges or edge_bd in forbidden_edges:
                    continue

                # pruning (cheap check)
                #if graph.distance(a, c) >= graph.distance(a, b):
                #continue

                # full cost comparison
                old_dist = graph.distance(a, b) + graph.distance(c, d)
                new_dist = graph.distance(a, c) + graph.distance(b, d)

                if new_dist < old_dist:
                    # perform 2-opt swap
                    best[i:j+1] = reversed(best[i:j+1])

                    # update position map efficiently
                    for idx in range(i, j + 1):
                        pos[best[idx]] = idx

                    improved = True
                    break
            if improved:
                break
        # repeat until no improvement

    return Path(best)


# --------------------------------------------------
# 2-opt for the full solution (both paths)
# --------------------------------------------------
def two_opt_solution(solution: Solution, graph: Graph) -> Solution:
    best = solution
    improved = True

    while improved:
        improved = False

        # improve path1
        forbidden1 = best.path2.edge_set()
        new_path1 = two_opt_path(best.path1, graph, forbidden1)
        if new_path1.total_distance(graph) < best.path1.total_distance(graph):
            candidate = Solution(new_path1, best.path2)
            if candidate.is_valid(graph):
                best = candidate
                improved = True
                continue

        # improve path2
        forbidden2 = best.path1.edge_set()
        new_path2 = two_opt_path(best.path2, graph, forbidden2)
        if new_path2.total_distance(graph) < best.path2.total_distance(graph):
            candidate = Solution(best.path1, new_path2)
            if candidate.is_valid(graph):
                best = candidate
                improved = True

    return best