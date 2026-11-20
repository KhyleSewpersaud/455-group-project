import random

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

POP_SIZE = 20
GENERATIONS = 100
MUTATION_RATE = 0.2
CROSSOVER_RATE = 0.9


# Physical keyboard coordinates (x, y). Used for fitness function
#
# x increases from left to right.
# y increases from top to bottom.
#
# Each row is horizontally staggered to approximate
# the physical arrangement of a standard keyboard.
#
# These positions never change during evolution.

KEY_POSITIONS = {
    # Top row (indices 0-9)
    0: (0.00, 0),
    1: (1.00, 0),
    2: (2.00, 0),
    3: (3.00, 0),
    4: (4.00, 0),
    5: (5.00, 0),
    6: (6.00, 0),
    7: (7.00, 0),
    8: (8.00, 0),
    9: (9.00, 0),
    # Middle row (indices 10-18)
    10: (0.25, 1),
    11: (1.25, 1),
    12: (2.25, 1),
    13: (3.25, 1),
    14: (4.25, 1),
    15: (5.25, 1),
    16: (6.25, 1),
    17: (7.25, 1),
    18: (8.25, 1),
    # Bottom row (indices 19-25)
    19: (0.75, 2),
    20: (1.75, 2),
    21: (2.75, 2),
    22: (3.75, 2),
    23: (4.75, 2),
    24: (5.75, 2),
    25: (6.75, 2),
    # Fixed semicolon key
    26: (9.25, 1),
}


# When typing, each key has an assigned finger that is supposed to press it.
# This maps each physical key index to its assigned finger.
#
# These assignments follow standard touch typing.
# They remain fixed even if the EA rearranges letters.

KEY_FINGERS = {
    # Top row
    0: "left_pinky",
    1: "left_ring",
    2: "left_middle",
    3: "left_index",
    4: "left_index",
    5: "right_index",
    6: "right_index",
    7: "right_middle",
    8: "right_ring",
    9: "right_pinky",
    # Middle row
    10: "left_pinky",
    11: "left_ring",
    12: "left_middle",
    13: "left_index",
    14: "left_index",
    15: "right_index",
    16: "right_index",
    17: "right_middle",
    18: "right_ring",
    # Bottom row
    19: "left_pinky",
    20: "left_ring",
    21: "left_middle",
    22: "left_index",
    23: "left_index",
    24: "right_index",
    25: "right_index",
    # Fixed semicolon
    26: "right_pinky",
}


# Each finger has a fixed resting position in touch typing technique.
#
# These values are physical key indices.
# They don't change when letters are rearranged.

HOME_KEY_INDICES = {
    "left_pinky": 10,  # A position
    "left_ring": 11,  # S position
    "left_middle": 12,  # D position
    "left_index": 13,  # F position
    "right_index": 16,  # J position
    "right_middle": 17,  # K position
    "right_ring": 18,  # L position
    "right_pinky": 26,  # Semicolon position
}

# Get the (x, y) coordinates of each finger's home key.
HOME_POSITIONS = {}

for finger, key_index in HOME_KEY_INDICES.items():
    home_position = KEY_POSITIONS[key_index]
    HOME_POSITIONS[finger] = home_position


def initialize_population(pop_size):
    """
    Generate a population of random keyboard layouts.

    Each individual is a permutation of the 26 letters.
    The index of each letter indicates which physical
    keyboard position it occupies.
    """
    population = []

    for i in range(pop_size):
        individual = random.sample(LETTERS, len(LETTERS))
        population.append(individual)

    return population


def get_letter_info(individual, letter):
    """
    Get physical information about a letter.

    Returns:
        - Physical key index
        - Key coordinates (x, y)
        - Assigned finger
        - Finger's home key index
        - Finger's home coordinates (x, y)
    """

    # Find the index of the letter in the genotype.
    # This index is also its physical keyboard position.
    key_index = individual.index(letter)

    # Find which finger presses this physical key.
    finger = KEY_FINGERS[key_index]

    # Get the coordinates of the key.
    key_position = KEY_POSITIONS[key_index]

    # Find where that finger normally rests.
    home_key_index = HOME_KEY_INDICES[finger]
    home_position = HOME_POSITIONS[finger]

    return {
        "key_index": key_index,
        "position": key_position,
        "finger": finger,
        "home_key_index": home_key_index,
        "home_position": home_position,
    }


def display_keyboard(individual):
    """Display the keyboard layout."""

    # Top row: indices 0-9
    print(" ".join(individual[0:10]))

    # Middle row: indices 10-18
    # Semicolon stays fixed.
    print(" " + " ".join(individual[10:19]) + " ;")

    # Bottom row: indices 19-25
    print("   " + " ".join(individual[19:26]))


# Fitness Evaluation - TODO
def fitness_keyboard():
    pass


# Mutation - TODO
def permutation_swap():
    pass


# Crossover - TODO
def permutation_pmx():
    pass


# Parent Selection - TODO
def tournament():
    pass


# Survivor Selection - TODO
def replacement():
    pass


def main():
    # Demonstrate that the representation works.
    population = initialize_population(POP_SIZE)

    individual = population[0]

    print("Genotype:")
    print(individual)

    print("\nPhenotype:")
    display_keyboard(individual)

    print("\nInformation about letter E:")
    print(get_letter_info(individual, "E"))


if __name__ == "__main__":
    main()
