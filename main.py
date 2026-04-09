from core.graph import Graph, make_edge, Edge

def main():
    graph = Graph.from_csv("input/random_50.csv")
    path1, path2 = nearest_neighbour(graph)
    print(score(graph, path1, path2))


# Returns the total distance of a path using the graph's distance cache
def path_distance(graph: Graph, path: list[int]) -> float:
    dist = sum(graph.distance(path[i], path[i+1]) for i in range(len(path) - 1))
    return round(dist, 2)

# Returns the score of two paths, defined as the larger of the two distances
def score(graph: Graph, path1: list[int], path2: list[int]) -> float:
    return max(path_distance(graph, path1), path_distance(graph, path2))

#Construct two disjoint paths over all cities using a greedy nearest-neighbour heuristic.
#Both paths start and end at city 0. At each step, both paths alternately extend to the
#nearest unvisited city, excluding edges already used by either path.
def nearest_neighbour(graph: Graph) -> tuple[list[int], list[int]]:
    used_edges: set[Edge] = set()

    path1 = [0]
    path2 = [0]

    unvisited1 = set(graph.city_ids) - {0}
    unvisited2 = set(graph.city_ids) - {0}

    while unvisited1 or unvisited2:
        for path, unvisited in [(path1, unvisited1), (path2, unvisited2)]:
            if not unvisited:
                continue
            current_city = path[-1]
            # get candidates sorted by distance, excluding already used edges
            candidates = graph.nearest_neighbours(current_city, exclude_edges=used_edges)
            # pick the nearest candidate not yet visited on this path
            next_city = next(c for c in candidates if c in unvisited)
            path.append(next_city)
            used_edges.add(make_edge(current_city, next_city))
            unvisited.remove(next_city)
    
    # close both loops back to the origin
    path1.append(0)
    path2.append(0)

    return path1, path2

if __name__ == "__main__":
    main()