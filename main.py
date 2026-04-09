import numpy as np
import pandas as pd
from core.graph import Graph, make_edge, Edge

def main():
    graph = Graph.from_csv("input/random_50.csv")
    path1, path2 = nearest_neighbour(graph)
    print(score(graph, path1, path2))

def path_distance(graph: Graph, path: list[int]) -> float:
    dist = sum(graph.distance(path[i], path[i+1]) for i in range(len(path) - 1))
    return round(dist, 2)

def score(graph: Graph, path1: list[int], path2: list[int]) -> float:
    return max(path_distance(graph, path1), path_distance(graph, path2))

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
            candidates = graph.nearest_neighbours(current_city, exclude_edges=used_edges)
            next_city = next(c for c in candidates if c in unvisited)
            path.append(next_city)
            used_edges.add(make_edge(current_city, next_city))
            unvisited.remove(next_city)
    
    path1.append(0)
    path2.append(0)

    return path1, path2

if __name__ == "__main__":
    main()