# Window and Capture Settings
WINDOW_NAME = "Bluestacks"
WINDOW_SIZE = {'width': 576, 'height': 1070}

# Confidence Thresholds
TEMPLATE_MATCHING_CONFIDENCE = 0.8
GAME_OVER_CONFIDENCE = 0.8

# Regions of Interest (ROI)
REGIONS = {
    "SHOP": (100, 923, 387, 1049),
    "ELIXIR": (398, 974, 461, 1044),
    "BENCH": (100, 800, 476, 900),  # Placeholder
    "FIELD": (100, 400, 476, 800),   # Placeholder
    "GAME_OVER": (100, 400, 476, 600) # Placeholder
}

# File Paths
TEMPLATE_PATH = "templates/cards"
GAME_OVER_PATH = "templates/game_over"

# Game Constants
BENCH_SIZE = 5
FIELD_ROWS = 3
FIELD_COLS = 5
FIELD_SIZE = FIELD_ROWS * FIELD_COLS
MERGE_DISTANCE_THRESHOLD = 50 # Max distance between two units to be considered for a merge
