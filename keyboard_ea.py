"""Master entry point for running customizable Keyboard EA experiments."""

import argparse
import random

from ea import (
    permutation_pmx,
    permutation_swap,
    replacement,
    run_ea,
    tournament,
)
from fitness import fitness_keyboard

# Default EA hyperparameters
DEFAULT_CONFIG = {
    "pop_size": 20,
    "generations": 100,
    "mutation_rate": 0.2,
    "crossover_rate": 0.9,
    "tournament_size": 4,
    "mating_pool_size": 10,
    "seed": None,
}


def display_keyboard(individual):
    """Display the keyboard layout."""
    # Top row: indices 0-9
    print(" ".join(individual[0:10]))

    # Middle row: indices 10-18 (semicolon stays fixed)
    print(" " + " ".join(individual[10:19]) + " ;")

    # Bottom row: indices 19-25
    print("   " + " ".join(individual[19:26]))


def parse_args():
    """Parse command-line options for customizing an EA run."""
    parser = argparse.ArgumentParser(
        description="Run the Evolutionary Keyboard Layout Optimizer."
    )
    parser.add_argument(
        "--pop-size",
        type=int,
        default=DEFAULT_CONFIG["pop_size"],
        help="Number of individuals in the population.",
    )
    parser.add_argument(
        "--generations",
        type=int,
        default=DEFAULT_CONFIG["generations"],
        help="Number of generations to evolve.",
    )
    parser.add_argument(
        "--mutation-rate",
        type=float,
        default=DEFAULT_CONFIG["mutation_rate"],
        help="Probability of mutating an offspring.",
    )
    parser.add_argument(
        "--crossover-rate",
        type=float,
        default=DEFAULT_CONFIG["crossover_rate"],
        help="Probability of applying crossover to a parent pair.",
    )
    parser.add_argument(
        "--tournament-size",
        type=int,
        default=DEFAULT_CONFIG["tournament_size"],
        help="Number of individuals sampled per tournament.",
    )
    parser.add_argument(
        "--mating-pool-size",
        type=int,
        default=DEFAULT_CONFIG["mating_pool_size"],
        help="Number of parents selected each generation.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_CONFIG["seed"],
        help="Optional random seed for reproducible runs.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-generation progress output.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    result = run_ea(
        pop_size=args.pop_size,
        generations=args.generations,
        mutation_rate=args.mutation_rate,
        crossover_rate=args.crossover_rate,
        tournament_size=args.tournament_size,
        mating_pool_size=args.mating_pool_size,
        fitness_fn=fitness_keyboard,
        mutation_fn=permutation_swap,
        crossover_fn=permutation_pmx,
        selection_fn=tournament,
        replacement_fn=replacement,
        verbose=not args.quiet,
    )

    best_solution = result["best_solution"]
    print(best_solution, "\n")
    display_keyboard(best_solution)


if __name__ == "__main__":
    main()
