from core.graph import Graph, Edge, make_edge

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