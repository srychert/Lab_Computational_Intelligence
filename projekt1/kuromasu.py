import numpy as np
import pygad

S = (11,11)
board = np.zeros(S[0]**2)
# initail board state
numbers = {
    (2, 0): 9,
    (8, 0): 8,
    (8, 1): 7,
    (4, 2): 12,
    (10, 2): 16,
    (0, 3): 9,
    (1, 4): 10,
    (2, 5): 12,
    (4, 5): 8,
    (6, 5): 11,
    (8, 5): 3,
    (9, 6): 3,
    (10, 7): 3,
    (0, 8): 7,
    (6, 8): 2,
    (2, 9): 7,
    (2, 10): 2,
    (8, 10): 5,
}
for key, value in numbers.items():
    board[key[0]*S[0] + key[1]] = value
print(board)

inital_population = []
for i in range(board.shape[0]):
    inital_population.append(board.flatten())

# print(inital_population)

#definiujemy parametry chromosomu
#geny to liczby: 0 lub 1
gene_space = [-1, 0]


#definiujemy funkcję fitness
def fitness_func(solution, solution_idx):
    # for idx, v in enumerate(solution):
    #     if
    return 0

fitness_function = fitness_func

#ile chromsomów w populacji - tablic z 0 i 1
#ile genow ma chromosom
sol_per_pop = 5
num_genes = len(board)**2

#ile wylaniamy rodzicow do "rozmanazania" (okolo 50% populacji)
#ile pokolen
#ilu rodzicow zachowac (kilka procent)
num_parents_mating = 5
num_generations = 30
keep_parents = 2

#jaki typ selekcji rodzicow?
#sss = steady, rws=roulette, rank = rankingowa, tournament = turniejowa
parent_selection_type = "sss"

#w il =u punktach robic krzyzowanie?
crossover_type = "single_point"

#mutacja ma dzialac na ilu procent genow?
#trzeba pamietac ile genow ma chromosom
mutation_type = "random"  # zamiana losowego genu
mutation_percent_genes = 1  # razy długość chromosomu troche powyżej 100 8 * 15

#inicjacja algorytmu z powyzszymi parametrami wpisanymi w atrybuty
ga_instance = pygad.GA(gene_space=gene_space,
                       gene_type=int,
                       num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes)

print("Initial Population")
# print(ga_instance.initial_population[0])

#uruchomienie algorytmu
ga_instance.run()

#podsumowanie: najlepsze znalezione rozwiazanie (chromosom+ocena)
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

#tutaj dodatkowo wyswietlamy sume wskazana przez jedynki
# prediction = np.sum(S*solution)
# print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))

#wyswietlenie wykresu: jak zmieniala sie ocena na przestrzeni pokolen
# ga_instance.plot_fitness()