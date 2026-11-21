"""Fitness functions and physical keyboard geometry for keyboard layout evaluation."""

# Physical keyboard coordinates (x, y). Used for fitness function.
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
HOME_POSITIONS = {
    finger: KEY_POSITIONS[key_index]
    for finger, key_index in HOME_KEY_INDICES.items()
}


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


# Evaluate fitness of an individual - TODO
def fitness_keyboard(individual):
    """Evaluate the fitness of a single keyboard layout."""
    pass


# Evaluate fitness of a list of individuals (e.g. population, offspring) - TODO
def fitness_batch(batch, fitness_fn=fitness_keyboard):
    """Evaluate fitness for each individual in a batch."""
    return [fitness_fn(indiv) for indiv in batch]
