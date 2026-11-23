"""Fitness functions and physical keyboard geometry for keyboard layout evaluation.

All geometry, finger assignments, resting distances, and transition costs are defined
strictly in terms of physical key locations (indices 0..25, plus 26 for resting right pinky),
completely independent of which letters are assigned to those locations.
The evolutionary algorithm mutates which letter occupies each physical key location.
"""

# Physical keyboard coordinates (x, y) for each key location index.
#
# x increases from left to right.
# y increases from top to bottom.
#
# Physical key location indices:
#   0-9:   Top row (10 key locations, left to right)
#   10-18: Middle/home row (9 letter key locations, left to right)
#   19-25: Bottom row (7 letter key locations, left to right)
#   26:    Right-most middle row resting location (non-letter home position for right pinky)
#
# These physical locations never change during evolution.
KEY_POSITIONS = {
    # Top row locations (indices 0-9)
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
    # Middle/home row locations (indices 10-18)
    10: (0.25, 1),
    11: (1.25, 1),
    12: (2.25, 1),
    13: (3.25, 1),
    14: (4.25, 1),
    15: (5.25, 1),
    16: (6.25, 1),
    17: (7.25, 1),
    18: (8.25, 1),
    # Bottom row locations (indices 19-25)
    19: (0.75, 2),
    20: (1.75, 2),
    21: (2.75, 2),
    22: (3.75, 2),
    23: (4.75, 2),
    24: (5.75, 2),
    25: (6.75, 2),
    # Fixed right-pinky resting location on middle row
    26: (9.25, 1),
}


# Maps each physical key location index to the finger that presses that location.
# These assignments depend only on physical key location, never on the letter placed there.
KEY_FINGERS = {
    # Top row locations (0-9)
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
    # Middle/home row locations (10-18)
    10: "left_pinky",
    11: "left_ring",
    12: "left_middle",
    13: "left_index",
    14: "left_index",
    15: "right_index",
    16: "right_index",
    17: "right_middle",
    18: "right_ring",
    # Bottom row locations (19-25)
    19: "left_pinky",
    20: "left_ring",
    21: "left_middle",
    22: "left_index",
    23: "left_index",
    24: "right_index",
    25: "right_index",
    # Right-pinky resting location
    26: "right_pinky",
}


# Physical key location index where each finger rests at home position.
HOME_KEY_INDICES = {
    "left_pinky": 10,   # Middle row, column 0
    "left_ring": 11,    # Middle row, column 1
    "left_middle": 12,  # Middle row, column 2
    "left_index": 13,   # Middle row, column 3
    "right_index": 16,  # Middle row, column 6
    "right_middle": 17, # Middle row, column 7
    "right_ring": 18,   # Middle row, column 8
    "right_pinky": 26,  # Middle row, column 9 (fixed semicolon position)
}

# (x, y) coordinates of each finger's resting home key location.
HOME_POSITIONS = {
    finger: KEY_POSITIONS[key_index]
    for finger, key_index in HOME_KEY_INDICES.items()
}


# ---------------------------------------------------------------------------
# Hardcoded Location Penalty Tables (strictly indexed by physical location 0..26)
# ---------------------------------------------------------------------------

# 1. Penalty for moving a finger from its resting home location to physical location `k`.
#    - 0 steps: Resting home locations (indices 10, 11, 12, 13, 16, 17, 18, 26)
#    - 1 step:  Locations one step from rest (indices 0, 1, 2, 3, 6, 7, 8, 9, 14, 15, 19, 20, 21, 22, 24, 25)
#    - 2 steps: Inner-column diagonal reach locations (indices 4, 5, 23)
HOME_DISTANCE_COST = {
    # Top row locations (0-9)
    0: 1, 1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1,
    # Middle row locations (10-18)
    10: 0, 11: 0, 12: 0, 13: 0, 14: 1, 15: 1, 16: 0, 17: 0, 18: 0,
    # Bottom row locations (19-25)
    19: 1, 20: 1, 21: 1, 22: 1, 23: 2, 24: 1, 25: 1,
    # Fixed right-pinky resting location (26)
    26: 0,
}

# 2. Pairwise movement costs between two physical key locations (loc1, loc2)
#    assigned to the SAME finger.
#    If two locations use DIFFERENT fingers, the transition cost between them is 0
#    (the previous finger returns to its resting location, and the next finger moves
#    from its own resting location using HOME_DISTANCE_COST).
_SAME_FINGER_LOCATION_DISTANCES = {
    # left_pinky physical locations: 0 (top), 10 (home), 19 (bottom)
    (0, 10): 1, (0, 19): 2, (10, 19): 1,
    # left_ring physical locations: 1 (top), 11 (home), 20 (bottom)
    (1, 11): 1, (1, 20): 2, (11, 20): 1,
    # left_middle physical locations: 2 (top), 12 (home), 21 (bottom)
    (2, 12): 1, (2, 21): 2, (12, 21): 1,
    # left_index physical locations: 3, 4 (top), 13 (home), 14 (middle inner), 22, 23 (bottom)
    (3, 4): 1, (3, 13): 1, (3, 14): 2, (3, 22): 2, (3, 23): 3,
    (4, 13): 2, (4, 14): 1, (4, 22): 2, (4, 23): 2,
    (13, 14): 1, (13, 22): 1, (13, 23): 2,
    (14, 22): 1, (14, 23): 1,
    (22, 23): 1,
    # right_index physical locations: 5, 6 (top), 15 (middle inner), 16 (home), 24, 25 (bottom)
    (5, 6): 1, (5, 15): 1, (5, 16): 2, (5, 24): 2, (5, 25): 3,
    (6, 15): 2, (6, 16): 1, (6, 24): 2, (6, 25): 2,
    (15, 16): 1, (15, 24): 1, (15, 25): 2,
    (16, 24): 1, (16, 25): 1,
    (24, 25): 1,
    # right_middle physical locations: 7 (top), 17 (home)
    (7, 17): 1,
    # right_ring physical locations: 8 (top), 18 (home)
    (8, 18): 1,
    # right_pinky physical locations: 9 (top), 26 (home)
    (9, 26): 1,
}

# Full 27x27 physical location lookup table: TRANSITION_COST_TABLE[loc1][loc2]
# - 0 whenever loc1 and loc2 use different fingers (or loc1 == loc2)
# - Step distance between loc1 and loc2 whenever they use the same finger
NUM_KEYS = len(KEY_POSITIONS)
TRANSITION_COST_TABLE = [
    [0 for _ in range(NUM_KEYS)] for _ in range(NUM_KEYS)
]

for (loc1, loc2), cost in _SAME_FINGER_LOCATION_DISTANCES.items():
    TRANSITION_COST_TABLE[loc1][loc2] = cost
    TRANSITION_COST_TABLE[loc2][loc1] = cost


# Tunable penalty weights for fitness calculation
SAME_FINGER_PENALTY = 1  # Extra penalty whenever the same finger is used consecutively
SHIFT_PENALTY = 1        # Extra penalty when Shift is required

# Placeholder sample text until the full evaluation corpus is plugged in
DEFAULT_SAMPLE_TEXT = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"


def get_transition_cost(key_loc1, key_loc2):
    """
    Return the penalty of moving directly from physical key_loc1 to key_loc2.

    Operates strictly on physical key location indices (0..26).
    Returns 0 if key_loc1 and key_loc2 use different fingers.
    """
    return TRANSITION_COST_TABLE[key_loc1][key_loc2]


def get_letter_info(individual, letter):
    """
    Look up which physical key location `letter` currently occupies in `individual`
    and return the physical properties of that key location.

    Returns:
        - Physical key location index (0..25)
        - Key coordinates (x, y)
        - Assigned finger for that physical location
        - Finger's home key location index
        - Finger's home coordinates (x, y)
    """
    # Find which physical key location index (0..25) currently holds this letter.
    key_index = individual.index(letter)

    # All physical properties below depend strictly on `key_index` (the location).
    finger = KEY_FINGERS[key_index]
    key_position = KEY_POSITIONS[key_index]
    home_key_index = HOME_KEY_INDICES[finger]
    home_position = HOME_POSITIONS[finger]

    return {
        "key_index": key_index,
        "position": key_position,
        "finger": finger,
        "home_key_index": home_key_index,
        "home_position": home_position,
    }


def fitness_keyboard(individual, sample_text=DEFAULT_SAMPLE_TEXT):
    """
    Evaluate the fitness of a keyboard layout on `sample_text`.

    How location-based evaluation works:
    ------------------------------------
    1. Map each letter in `individual` to its current physical key location index (0..25):
           letter_to_location = {letter: loc_idx for loc_idx, letter in enumerate(individual)}
    2. Walk through `sample_text`, translating each character into its physical location
       `curr_loc = letter_to_location[char]`.
    3. All cost lookups use `prev_loc` and `curr_loc` (the physical key locations):
       - If `prev_loc` and `curr_loc` use the SAME finger (`KEY_FINGERS[prev_loc] == KEY_FINGERS[curr_loc]`):
           total_penalty += SAME_FINGER_PENALTY + TRANSITION_COST_TABLE[prev_loc][curr_loc]
       - Otherwise (different fingers, or first key after reset):
           # Transition cost between different fingers is 0; finger starts from its resting home key.
           total_penalty += HOME_DISTANCE_COST[curr_loc]
    4. Return `-total_penalty` so higher fitness = lower total movement/penalty (0 is ideal).
    """
    if not sample_text:
        return 0

    # Map each letter ('A'..'Z') to its physical key location (0..25) in this individual
    letter_to_location = {
        letter: loc_idx for loc_idx, letter in enumerate(individual)
    }

    total_penalty = 0
    prev_loc = None

    for raw_ch in sample_text:
        ch = raw_ch.upper()
        if ch not in letter_to_location:
            # Non-letter / space: fingers return to their resting home positions
            prev_loc = None
            continue

        curr_loc = letter_to_location[ch]

        if prev_loc is not None and KEY_FINGERS[prev_loc] == KEY_FINGERS[curr_loc]:
            # Consecutive use of the same finger:
            # Penalize same-finger repeat + direct movement between prev_loc and curr_loc
            total_penalty += SAME_FINGER_PENALTY
            total_penalty += TRANSITION_COST_TABLE[prev_loc][curr_loc]
        else:
            # Different finger (or start of word):
            # Transition between fingers is 0; finger moves from its resting location to curr_loc
            total_penalty += HOME_DISTANCE_COST[curr_loc]

        prev_loc = curr_loc

    # Negate penalty so the EA maximizes fitness (less penalty = higher fitness)
    return -total_penalty


def fitness_batch(batch, fitness_fn=fitness_keyboard):
    """Evaluate fitness for each individual in a batch."""
    return [fitness_fn(indiv) for indiv in batch]
