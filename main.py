from core.graph import Graph
from algorithms.nearest_neighbour import nearest_neighbour
from algorithms.two_opt import two_opt_solution
from algorithms.k_opt import k_opt
from algorithms.simulated_annealing import simulated_annealing
from algorithms.generic_algorithm import genetic_algorithm
from algorithms.hill_climbing import hill_climbing

import os

def main():
    file_name = input("Input file name (default random_50): ")
    file_name = "input/random_50.csv" if file_name == "" else "input/" + file_name + ".csv"
    if not os.path.exists(file_name):
        print("File does not exist")
        return
    graph = Graph.from_csv(file_name)

    # Precompute candidate lists for 2-opt (critical for performance on larger instances)
    graph.compute_candidate_lists(k=20)  
    
    print("[1] Greedy")
    print("[2] 2-opt")
    print("[3] K-opt (ILS)")
    print("[4] Simulated Annealing")
    print("[5] Genetic Algorithm")
    print("[6] Hill Climbing")
    alg = input("Choose an algorithm: ")
    
    if alg == "1":
        sol = nearest_neighbour(graph)
    elif alg == "2":
        initial_sol = nearest_neighbour(graph)
        sol = two_opt_solution(initial_sol, graph)
    elif alg == "3":
        initial_sol = nearest_neighbour(graph)
        sol = two_opt_solution(initial_sol, graph)
        sol = k_opt(sol, graph, iterations=50, k=3)
    elif alg == "4":
        initial_sol = nearest_neighbour(graph)
        sol = two_opt_solution(initial_sol, graph)
        sol = simulated_annealing(sol, graph, iterations=1000, k=2)
    elif alg == "5":
        sol = genetic_algorithm(graph, population_size=50, max_no_improve=100)
    elif alg == "6":
        sol = hill_climbing(graph, n_restarts=50)
    else:
        print("Invalid algorithm")
        return

    dist1, dist2 = sol.distances(graph)
    print(f"Path1 distance: {dist1}, Path2 distance: {dist2}")
    print(f"Score: {sol.score(graph)}")

if __name__ == "__main__":
    main()