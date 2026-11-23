"""Evolutionary algorithm operators and main evolution loop.

Each individual is a list of 26 letters where the list index (0..25) represents
the physical key location on the keyboard, and the element at that index is the
letter currently assigned to that location.
Mutations and crossover rearrange which physical key locations the letters occupy.
"""

import random

from fitness import fitness_batch, fitness_keyboard

# The 26 letters that are assigned to physical key locations 0..25.
LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Physical key location layout:
#   0-9:   Top row locations, left to right
#   10-18: Middle/home row locations, left to right
#   19-25: Bottom row locations, left to right
#   (Location 26 is the fixed right-pinky resting location, not part of the 26-letter genotype)


def initialize_population(pop_size, letters=LETTERS):
    """
    Generate a population of random keyboard layouts.

    Each individual is a permutation of the 26 letters across physical locations 0..25.
    """
    population = []

    for _ in range(pop_size):
        individual = random.sample(letters, len(letters))
        population.append(individual)

    return population


def permutation_swap(indiv):
    """
    Swap mutation: pick two physical key locations (0..25) and swap the letters
    assigned to those two locations in-place.
    """
    first_loc, second_loc = random.sample(range(len(indiv)), 2)
    indiv[first_loc], indiv[second_loc] = indiv[second_loc], indiv[first_loc]
    return indiv


def _pmx_single(parent1, parent2, cut1, cut2):
    """Construct one valid permutation child using Partially Mapped Crossover (PMX)."""
    size = len(parent1)
    child = [None] * size

    # 1. Copy the slice of physical locations [cut1:cut2] directly from parent1
    child[cut1:cut2] = parent1[cut1:cut2]

    # Map each letter in parent1's slice to the corresponding letter in parent2's slice
    p1_to_p2 = {parent1[loc]: parent2[loc] for loc in range(cut1, cut2)}
    copied_letters = set(child[cut1:cut2])

    # 2. For the remaining locations in the slice of parent2, place any letter not yet
    #    in `child` by following the PMX mapping chain to an open physical location.
    for loc in range(cut1, cut2):
        candidate = parent2[loc]
        if candidate not in copied_letters:
            target_letter = parent1[loc]
            target_loc = parent2.index(target_letter)
            while child[target_loc] is not None:
                target_letter = parent1[target_loc]
                target_loc = parent2.index(target_letter)
            child[target_loc] = candidate
            copied_letters.add(candidate)

    # 3. Fill any remaining open physical locations directly from parent2
    for loc in range(size):
        if child[loc] is None:
            child[loc] = parent2[loc]

    return child


def permutation_pmx(parent1, parent2):
    """
    Partially Mapped Crossover (PMX) for two parent keyboard layouts.

    Preserves absolute physical key locations from both parents while ensuring
    every letter A-Z appears at exactly one location in each child.

    Returns:
        (child1, child2)
    """
    size = len(parent1)
    cut1, cut2 = sorted(random.sample(range(size), 2))
    if cut1 == cut2:
        cut2 = min(size, cut1 + 1)

    child1 = _pmx_single(parent1, parent2, cut1, cut2)
    child2 = _pmx_single(parent2, parent1, cut1, cut2)
    return child1, child2


def tournament(fitness, tournament_size=4, mating_pool_size=10):
    """
    k-Tournament selection for parent selection and loser identification.

    - Selects `mating_pool_size` parent indices by running tournaments of size
      `tournament_size` and picking the highest-fitness individual in each tournament.
    - Selects up to `mating_pool_size` distinct low-fitness replacement indices (`losers`)
      via inverse tournaments while protecting the global best (elite) individual.

    Returns:
        (selected_parent_indices, loser_indices_to_replace)
    """
    pop_size = len(fitness)
    k = min(tournament_size, pop_size)

    # 1. Select parents (winners of k-tournaments)
    selected = []
    while len(selected) < mating_pool_size:
        contenders = random.sample(range(pop_size), k)
        winner = max(contenders, key=lambda idx: fitness[idx])
        selected.append(winner)

    # 2. Select distinct replacement candidates (losers of k-tournaments),
    #    excluding the best (elite) individual in the population.
    elite_idx = max(range(pop_size), key=lambda idx: fitness[idx])
    non_elite_pool = [idx for idx in range(pop_size) if idx != elite_idx]
    num_to_replace = min(mating_pool_size, len(non_elite_pool))

    losers = []
    available = list(non_elite_pool)
    while len(losers) < num_to_replace and available:
        sample_k = min(k, len(available))
        contenders = random.sample(available, sample_k)
        loser = min(contenders, key=lambda idx: fitness[idx])
        losers.append(loser)
        available.remove(loser)

    return selected, losers


def replacement(offspring, to_replace, population):
    """
    Replace the selected tournament losers in `population` with `offspring`.

    Parameters:
        offspring: list of newly created child individuals
        to_replace: list of population indices to overwrite
        population: the current population list (modified in-place)
    """
    limit = min(len(offspring), len(to_replace))
    for i in range(limit):
        population[to_replace[i]] = offspring[i]


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

    # Start baseline comparison from standard QWERTY letter arrangement
    best_solution = list("QWERTYUIOPASDFGHJKLZXCVBNM")
    best_fit = fitness_fn(best_solution)
    best_gen = 0

    # Check if initial population already beats the baseline
    init_max = max(population_fitness)
    if init_max >= best_fit:
        best_solution = list(population[population_fitness.index(init_max)])
        best_fit = init_max

    if verbose:
        print(
            "Generation",
            str(current_gen).zfill(3),
            ": Best of generation",
            init_max,
            "\tGeneration average",
            sum(population_fitness) / pop_size,
        )

    # Begin evolution
    while current_gen < generations:
        current_gen += 1

        # 1. Parent & replacement-target selection via tournament
        parent_indices, losers = selection_fn(
            population_fitness,
            tournament_size=tournament_size,
            mating_pool_size=mating_pool_size,
        )

        # 2. Randomly pair parents by shuffling the mating pool
        random.shuffle(parent_indices)

        # 3. Reproduce / recombine (PMX crossover)
        offspring = []
        for i in range(0, len(parent_indices), 2):
            p1 = population[parent_indices[i]]
            p2 = population[parent_indices[(i + 1) % len(parent_indices)]]

            if random.random() < crossover_rate:
                child1, child2 = crossover_fn(p1, p2)
            else:
                child1, child2 = list(p1), list(p2)

            offspring.append(child1)
            if len(offspring) < len(parent_indices):
                offspring.append(child2)

        # 4. Mutate (swap letters between two physical key locations)
        for child in offspring:
            if random.random() < mutation_rate:
                mutation_fn(child)

        # 5. Survivor selection / replacement (with elitism protection)
        replacement_fn(offspring, losers, population)

        # 6. Re-evaluate fitnesses
        population_fitness = fitness_batch(population, fitness_fn=fitness_fn)
        pop_max = max(population_fitness)
        if pop_max >= best_fit:
            best_solution = list(population[population_fitness.index(pop_max)])
            best_fit = pop_max
            best_gen = current_gen

        if verbose:
            print(
                "Generation",
                str(current_gen).zfill(3),
                ": Best of generation",
                pop_max,
                "\tGeneration average",
                sum(population_fitness) / pop_size,
            )

    return {
        "best_solution": best_solution,
        "best_fitness": best_fit,
        "best_generation": best_gen,
        "population": population,
    }
