"""Evolutionary algorithm operators and main evolution loop."""

import random

from fitness import fitness_batch, fitness_keyboard

# The 26 letters that can be rearranged.
LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Each individual is a list of 26 letters.
# The index determines the physical keyboard position:
#
# 0-9:   Top row, left to right
# 10-18: Middle row, left to right
# 19-25: Bottom row, left to right
#
# Index 26 is reserved for the fixed semicolon position.
# It is NOT included in the genotype.


def initialize_population(pop_size, letters=LETTERS):
    """
    Generate a population of random keyboard layouts.

    Each individual is a permutation of the 26 letters.
    The index of each letter indicates which physical
    keyboard position it occupies.
    """
    population = []

    for _ in range(pop_size):
        individual = random.sample(letters, len(letters))
        population.append(individual)

    return population


# Mutation - TODO
def permutation_swap(indiv):
    """Pick two random indices and swap the characters at them."""
    first = random.randint(0, len(indiv) - 1)
    second = random.randint(0, len(indiv) - 1)
    indiv[first], indiv[second] = indiv[second], indiv[first]


# Crossover - TODO
def permutation_pmx():
    """Partially Mapped Crossover (PMX) for permutation genotypes."""
    pass


# Parent Selection - TODO
def tournament(fitness, tournament_size=4, mating_pool_size=10):
    """Select parents and replacement candidates via tournament selection."""
    selected = []
    losers = random.sample(range(0, len(fitness)), tournament_size)
    while len(selected) < mating_pool_size:
        pass  # selecting

    return selected, losers


# Survivor Selection - TODO
def replacement(offspring, to_replace, population):
    """
    Replaces losers of tournament with new individuals.

    Parameters:
        offspring: the individuals that are being added
        to_replace: a list of indices for the individuals in population to be replaced
        population: the actual population where new individuals are added
    Usage:
        e.g. population[to_replace[i]] = offspring[i]
    """
    pass


def run_ea(
    pop_size=20,
    generations=100,
    mutation_rate=0.2,
    crossover_rate=0.9,
    tournament_size=4,
    mating_pool_size=10,
    fitness_fn=fitness_keyboard,
    mutation_fn=permutation_swap,
    crossover_fn=permutation_pmx,
    selection_fn=tournament,
    replacement_fn=replacement,
    verbose=True,
):
    """
    Run the evolutionary algorithm with configurable hyperparameters and operators.

    Returns:
        dict with keys: best_solution, best_fitness, best_generation, population
    """
    current_gen = 0
    population = initialize_population(pop_size)
    population_fitness = fitness_batch(population, fitness_fn=fitness_fn)
    best_solution = list("QWERTYUIOPASDFGHJKLZXCVBNM")
    best_fit = fitness_fn(best_solution)
    best_gen = -1

    if verbose:
        print(
            "Generation",
            current_gen,
            ": Best of generation",
            max(population_fitness),
            "\tGeneration average",
            sum(population_fitness) / pop_size,
        )

    # Begin evolution
    while current_gen < generations:
        current_gen += 1

        # Parent selection
        parent_indices, losers = selection_fn(
            population_fitness,
            tournament_size=tournament_size,
            mating_pool_size=mating_pool_size,
        )

        # Randomly pair by shuffling
        random.shuffle(parent_indices)

        # Reproduce/recombine - TODO (use crossover_rate and crossover_fn)

        # Mutate - TODO (use mutation_rate and mutation_fn)

        # Replace - TODO (use replacement_fn)

        # Re-evaluate fitnesses
        population_fitness = fitness_batch(population, fitness_fn=fitness_fn)
        pop_max = max(population_fitness)
        if pop_max >= best_fit:
            best_solution = population[population_fitness.index(pop_max)]
            best_fit = pop_max
            best_gen = current_gen

    return {
        "best_solution": best_solution,
        "best_fitness": best_fit,
        "best_generation": best_gen,
        "population": population,
    }
