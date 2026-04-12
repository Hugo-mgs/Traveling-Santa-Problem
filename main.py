from core.graph import Graph
from algorithms.nearest_neighbour import nearest_neighbour
from algorithms.two_opt import two_opt_solution
from algorithms.k_opt import k_opt
from algorithms.simulated_annealing import simulated_annealing
from algorithms.genetic_algorithm import genetic_algorithm
from algorithms.hill_climbing import hill_climbing

from timeit import default_timer as timer
import os

def main():
    file_name = input("Input file name (default santa_100): ")
    file_name = "input/santa_100.csv" if file_name == "" else "input/" + file_name + ".csv"
    if not os.path.exists(file_name):
        print("File does not exist")
        return
    graph = Graph.from_csv(file_name)

    
    print("[1] Greedy")
    print("[2] 2-opt")
    print("[3] K-opt (ILS)")
    print("[4] Simulated Annealing")
    print("[5] Genetic Algorithm")
    print("[6] Hill Climbing")
    alg = input("Choose an algorithm: ")

    start = timer()
    
    if not alg == "1":
        # Precompute candidate lists for 2-opt (critical for performance on larger instances)
        graph.compute_candidate_lists(k=20)  
    
    if alg == "1":
        sol = nearest_neighbour(graph)
    elif alg == "2":
        initial_sol = nearest_neighbour(graph)
        sol = two_opt_solution(initial_sol, graph)
    elif alg == "3":
        it = int(input("Number of iterations: "))
        k = int(input("K: "))
        initial_sol = nearest_neighbour(graph)
        sol = two_opt_solution(initial_sol, graph)
        sol = k_opt(sol, graph, iterations=it, k=k)
    elif alg == "4":
        it = int(input("Number of iterations: "))
        k = int(input("K: "))
        initial_sol = nearest_neighbour(graph)
        sol = two_opt_solution(initial_sol, graph)
        sol = simulated_annealing(sol, graph, iterations=it, k=k)
    elif alg == "5":
        pop_size = int(input("Population size: "))
        no_imp = int(input("Max of no improves: "))
        sol = genetic_algorithm(graph, population_size=pop_size, max_no_improve=no_imp)
    elif alg == "6":
        n = int(input("Number of restarts: "))
        sol = hill_climbing(graph, n_restarts=n)
    else:
        print("Invalid algorithm")
        return
    
    end = timer()

    dist1, dist2 = sol.distances(graph)
    print(f"Path1 distance: {dist1}, Path2 distance: {dist2}")
    print(f"Score: {sol.score(graph)}")
    print(f"Time elapsed: {round(end - start, 2)}s")
    output_filename = "solution.csv"
    sol.to_csv(output_filename)
    print(f"Solution saved to {output_filename}")

if __name__ == "__main__":
    main()