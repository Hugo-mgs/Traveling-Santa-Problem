from core.graph import Graph
from core.nearest_neighbour import nearest_neighbour

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

if __name__ == "__main__":
    main()