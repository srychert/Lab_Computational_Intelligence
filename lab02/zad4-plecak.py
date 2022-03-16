import pygad
import numpy

S = [1, 2, 3, 6, 10, 17, 25, 29, 30, 41, 51, 60, 70, 79, 80]

slimak = {
    "nazwy": ["zegar", "obraz-pejzaz", "obraz-portret", "radio", "laptop", "lampka nocna", "srebrne sztuće",
              "porcelana", "figura z brązu", "skórzana torebka", "odkurzacz"],
    "wartosc": [100, 300, 200, 40, 500, 70, 100, 250, 300, 280, 300],
    "waga": [7, 7, 6, 2, 5, 6, 1, 3, 10, 3, 15]
}

# definiujemy parametry chromosomu
# geny to liczby: 0 lub 1
gene_space = [0, 1]


# definiujemy funkcję fitness
def fitness_func(solution, solution_idx):
    if numpy.sum(solution * slimak["waga"]) >= 25:
        return 0
    return numpy.sum(solution * slimak["wartosc"])


fitness_function = fitness_func

# ile chromsomów w populacji - tablic z 0 i 1
# ile genow ma chromosom
sol_per_pop = 15
num_genes = len(slimak["wartosc"])

# ile wylaniamy rodzicow do "rozmanazania" (okolo 50% populacji)
# ile pokolen
# ilu rodzicow zachowac (kilka procent)
num_parents_mating = 5
num_generations = 50
keep_parents = 2

# jaki typ selekcji rodzicow?
# sss = steady, rws=roulette, rank = rankingowa, tournament = turniejowa
parent_selection_type = "sss"

# w il =u punktach robic krzyzowanie?
crossover_type = "single_point"

# mutacja ma dzialac na ilu procent genow?
# trzeba pamietac ile genow ma chromosom
mutation_type = "random"  # zamiana losowego genu
mutation_percent_genes = 10  # razy długość chromosomu troche powyżej 100 10 * 11

# inicjacja algorytmu z powyzszymi parametrami wpisanymi w atrybuty
ga_instance = pygad.GA(gene_space=gene_space,
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

# uruchomienie algorytmu
ga_instance.run()

# podsumowanie: najlepsze znalezione rozwiazanie (chromosom+ocena)
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

# tutaj dodatkowo wyswietlamy sume wskazana przez jedynki
prediction = numpy.sum(slimak["wartosc"] * solution)
print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))

# przedmioty
t = []
for idx, val in enumerate(solution):
    if val == 1:
        t.append(slimak["nazwy"][idx])
print("Coresponding items: {t}".format(t=t))

# wyswietlenie wykresu: jak zmieniala sie ocena na przestrzeni pokolen
ga_instance.plot_fitness()
