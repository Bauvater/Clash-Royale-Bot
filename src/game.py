from config import REGIONS

class GameInfo:
    def __init__(self):
        self.characters = ("archer_queen", "archer", "baby_dragon",
                           "bandit", "barbarian", "dart_goblin",
                           "electro_giant", "electro_wizard", "executioner",
                           "giant_skeleton", "goblin_machine", "goblin",
                           "golden_knight", "knight", "mega_knight",
                           "musketeer", "pekka", "prince",
                           "princess", "royal_ghost", "skeleton_dragons",
                           "skeleton_king", "spear_goblin", "valkyrie",
                           "witch", "wizard")
        self.regions = REGIONS

class GameState:
    def __init__(self):
        self.player_health = 10
        self.elixir = 0
        self.shop_characters = []
        self.bench_characters = []
        self.field_characters = []
