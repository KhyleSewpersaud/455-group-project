"""Fitness functions and physical keyboard geometry for keyboard layout evaluation.

All geometry, finger assignments, resting distances, and transition costs are defined
strictly in terms of physical key locations (indices 0..25, plus 26 for resting right pinky),
completely independent of which letters are assigned to those locations.
The evolutionary algorithm mutates which letter occupies each physical key location.
"""

from math import sqrt

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

# Full 27x27 physical location lookup table: TRANSITION_COST_TABLE[loc1][loc2]
# - 0 whenever loc1 and loc2 use different fingers (or loc1 == loc2)
# - Step distance between loc1 and loc2 whenever they use the same finger
NUM_KEYS = len(KEY_POSITIONS)

# Precomputes distances of all position pairs for lookup later on
def precompute_distance_lookup() -> dict:
    lookup = {}
    for i in range(NUM_KEYS):
        for j in range(NUM_KEYS):
            # Euclidean distance between each key pair
            (x1, y1) = KEY_POSITIONS[i]
            (x2, y2) = KEY_POSITIONS[j]
            dist = sqrt( (x2-x1)**2 + (y2-y1)**2 )
            lookup[(i, j)] = dist
    return lookup

DISTANCE_LOOKUP = precompute_distance_lookup()
# print(DISTANCE_LOOKUP)


# Placeholder sample text until the full evaluation corpus is plugged in
SAMPLE_TEXTS = [
    "EVERY YOUNG ZEBRA QUICKLY EXPLORES VAST JUNGLES WHILE EXAMINING COLORFUL FUNGI AND OBSERVING HOW COMPLEX ECOSYSTEMS FLOURISH BENEATH THE BLAZING SUN",
    "BEYOND DISTANT GALAXIES MYSTERIOUS QUASARS EMIT BRILLIANT ULTRAVIOLET RADIATION WHILE ASTRONOMERS EXAMINE COSMIC PHENOMENA AND INVESTIGATE WHETHER EXTRATERRESTRIAL LIFE EXISTS",
    "MATHEMATICIANS FREQUENTLY ANALYZE COMPLEX EQUATIONS BY UTILIZING NUMERICAL SEQUENCES AND QUADRATIC FUNCTIONS TO QUANTIFY PATTERNS AND SOLVE PERPLEXING PROBLEMS WITH PRECISION",
    "DURING MEDIEVAL TIMES BRAVE KNIGHTS JOURNEYED ACROSS VAST KINGDOMS WHERE QUEENS GOVERNED ANCIENT CITIES AND MERCHANTS EXCHANGED EXOTIC JEWELS FOR VALUABLE RESOURCES",
    "WHEN OXYGEN COMBINES WITH HYDROGEN UNDER SPECIFIC CONDITIONS ENERGETIC REACTIONS YIELD WATER WHILE SCIENTISTS QUANTIFY MOLECULAR CHANGES USING PRECISE LABORATORY EQUIPMENT",
    "EXPLORERS FREQUENTLY TRAVERSE RUGGED MOUNTAINS AND VAST DESERTS TO EXAMINE GEOGRAPHIC FEATURES WHILE DOCUMENTING UNIQUE CLIMATES AND DISCOVERING UNFAMILIAR WILDLIFE",
    "QUANTUM MECHANICS EXAMINES HOW PARTICLES BEHAVE WHEN ENERGY FLUCTUATES THROUGH MICROSCOPIC ENVIRONMENTS WHERE UNCERTAINTY CHALLENGES CLASSICAL EXPLANATIONS OF PHYSICAL PHENOMENA",
    "HUMAN BEHAVIOR INVOLVES COMPLEX COGNITIVE PROCESSES WHEREBY EMOTIONS INFLUENCE JUDGMENT WHILE RESEARCHERS EXAMINE MEMORY MOTIVATION AND ANXIETY THROUGH CAREFULLY DESIGNED EXPERIMENTS",
    "LINGUISTS INVESTIGATE HOW DIVERSE LANGUAGES EVOLVE THROUGH PHONETIC SHIFTS GRAMMATICAL STRUCTURES AND VOCABULARY EXCHANGES WHILE EXAMINING QUIRKY EXPRESSIONS ACROSS GLOBAL COMMUNITIES",
    "PROGRAMMERS DEVELOP EFFICIENT ALGORITHMS THAT ORGANIZE VAST QUANTITIES OF INFORMATION WHILE DEBUGGING COMPLEX SOFTWARE AND EXPLORING INNOVATIVE TECHNOLOGIES THROUGH EXPERIMENTAL PROJECTS"
]

PENALTY_INCREASE = 1
PENALTY_MIN = 2


# def get_transition_cost(key_loc1, key_loc2):
#     """
#     Return the penalty of moving directly from physical key_loc1 to key_loc2.

#     Operates strictly on physical key location indices (0..26).
#     Returns 0 if key_loc1 and key_loc2 use different fingers.
#     """
#     return TRANSITION_COST_TABLE[key_loc1][key_loc2]


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


def fitness_keyboard(individual, sample_texts=SAMPLE_TEXTS):
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
    if not sample_texts:
        return 0

    # Map each letter ('A'..'Z') to its physical key location (0..25) in this individual
    letter_to_location = {
        letter: loc_idx for loc_idx, letter in enumerate(individual)
    }

    fitness = 0

    for sample_text in sample_texts:
        penalty = PENALTY_MIN
        prev_loc = None
        for ch in sample_text: 
            if ch not in letter_to_location:
                # Non-letter / space: fingers return to their resting home positions
                prev_loc = None
                continue
        
            curr_loc = letter_to_location[ch]
        
            if prev_loc is not None and KEY_FINGERS == KEY_FINGERS[curr_loc]:
                # Consecutive use of same finger
                # Penalize same-finger repeat and raise sequential penalty multiplier
                fitness += DISTANCE_LOOKUP[(prev_loc, curr_loc)] * penalty
                penalty += PENALTY_INCREASE
                continue
            else: 
                # Reset penalty multiplier
                penalty = PENALTY_MIN

            if prev_loc == curr_loc:
                # Same key -> no distance traveled
                continue
            else:
                # Different finger/start of word (means finger returned to home)
                # print(KEY_FINGERS[curr_loc])
                # print(HOME_KEY_INDICES[KEY_FINGERS[curr_loc]], curr_loc)
                home_key = HOME_KEY_INDICES[KEY_FINGERS[curr_loc]]
                fitness += DISTANCE_LOOKUP[(home_key, curr_loc)]

        
            prev_loc = curr_loc

    # Negate fitness so the EA maximizes fitness (less penalty = higher fitness)
    return -fitness


def fitness_batch(batch, fitness_fn=fitness_keyboard):
    """Evaluate fitness for each individual in a batch."""
    return [fitness_fn(indiv) for indiv in batch]
