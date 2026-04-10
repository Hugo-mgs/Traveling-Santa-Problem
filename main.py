from core.graph import Graph
from algorithms.nearest_neighbour import nearest_neighbour

import os

def main():
    file_name = input("Input file name (default random_50): ")
    file_name = "input/random_50.csv" if file_name == "" else "input/" + file_name + ".csv"
    if not os.path.exists(file_name):
        print("File does not exist")
        return
    graph = Graph.from_csv(file_name)
    
    print("[1] Greedy")
    alg = input("Choose an algorithm: ")
    
    if alg == "1":
        sol = nearest_neighbour(graph)
    else:
        print("Invalid algorithm")
        return

    dist1, dist2 = sol.distances(graph)
    print(f"Path1 distance: {dist1}, Path2 distance: {dist2}")
    print(f"Score: {sol.score(graph)}")

if __name__ == "__main__":
    main()