import random
from core.graph import Graph
from core.solution import Solution, Path
from algorithms.two_opt import two_opt_solution
from algorithms.nearest_neighbour import nearest_neighbour
from algorithms.crossover import crossover, fix_shared_edges

 #Generate a random solution 
def random_solution(graph: Graph) -> Solution:
    cities = [c for c in graph.city_ids if c != 0]
    path1 = [0] + random.sample(cities, len(cities)) + [0]
    path2 = [0] + random.sample(cities, len(cities)) + [0]
    return Solution(Path(path1), Path(path2))


#Seed population with one nearest-neighbour solution, rest random.
def initialise_population(graph: Graph, size: int) -> list[Solution]:
    seed = two_opt_solution(nearest_neighbour(graph), graph)
    population = [seed]
    while len(population) < size:
        population.append(random_solution(graph))
    return population


#Pick tournament_size random candidates and return the best one.
def tournament_selection(population: list[Solution], graph: Graph, tournament_size: int = 3) -> Solution:
    candidates = random.sample(population, tournament_size)
    return min(candidates, key=lambda s: s.score(graph))

#Mutate a solution by applying two-opt with some probability.
def mutate(solution: Solution, graph: Graph) -> Solution:
    if random.random() < 0.3:
        return two_opt_solution(solution, graph)
    return solution


#Run the genetic algorithm until no improvement for max_no_improve generations.
def genetic_algorithm(graph: Graph, population_size: int = 50, max_no_improve: int = 100) -> Solution:
    population = initialise_population(graph, population_size)
    best = min(population, key=lambda s: s.score(graph))

    no_improve = 0
    while no_improve < max_no_improve:
        new_population = [best]

        for _ in range(population_size):
            # select two parents using tournament selection
            parent1 = tournament_selection(population, graph)
            parent2 = tournament_selection(population, graph)

            # linear order crossover to produce a child solution
            child = crossover(parent1, parent2)
            # repair disjointness violations
            child = fix_shared_edges(child)
            # mutate the child solution using two-opt with some probability
            child = mutate(child, graph)
            new_population.append(child)

        population = new_population
        candidate = min(population, key=lambda s: s.score(graph))

        if candidate.score(graph) < best.score(graph):
            best = candidate
            no_improve = 0
        else:
            no_improve += 1

    return best