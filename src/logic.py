from config import BENCH_SIZE, FIELD_SIZE, MERGE_DISTANCE_THRESHOLD
from collections import defaultdict
import random
import math

class Tactics:
    def __init__(self, game_state, game_info, ki):
        self.game_state = game_state
        self.game_info = game_info
        self.ki = ki
        self.current_strategy = self.ki.get_best_strategy() or "default"

    def make_decision(self):
        if self.current_strategy == "default":
            return self.default_strategy()
        # Add other strategies here
        else:
            return self.default_strategy()

    def default_strategy(self):
        # Merge units if possible
        merge_action = self.find_merge_opportunity()
        if merge_action:
            return merge_action

        # Place units on the field if there's space
        if len(self.game_state.field_characters) < FIELD_SIZE:
            place_action = self.place_unit()
            if place_action:
                return place_action

        # Buy units if the bench is not full and we have enough elixir
        if len(self.game_state.bench_characters) < BENCH_SIZE:
            if self.game_state.elixir >= 1:
                if self.game_state.shop_characters[0]:
                    return "buy_slot_1"
                if self.game_state.shop_characters[1]:
                    return "buy_slot_2"
                if self.game_state.shop_characters[2]:
                    return "buy_slot_3"
        return None

    def find_merge_opportunity(self):
        # Group bench characters by type
        units_by_type = defaultdict(list)
        for unit, coords in self.game_state.bench_characters:
            units_by_type[unit].append(coords)

        for unit, coords_list in units_by_type.items():
            if len(coords_list) >= 2:
                # Find two units of the same type that are close to each other
                for i in range(len(coords_list)):
                    for j in range(i + 1, len(coords_list)):
                        coord1 = coords_list[i]
                        coord2 = coords_list[j]
                        if math.dist(coord1, coord2) < MERGE_DISTANCE_THRESHOLD:
                            return f"merge_{unit}_{coord1[0]}_{coord1[1]}_{coord2[0]}_{coord2[1]}"
        return None

    def place_unit(self):
        if self.game_state.bench_characters:
            unit_to_place, bench_coords = self.game_state.bench_characters[0]

            # Find an empty field slot (simple placement in the first available slot for now)
            occupied_field_slots = len(self.game_state.field_characters)
            if occupied_field_slots < FIELD_SIZE:
                row = occupied_field_slots // 5
                col = occupied_field_slots % 5
                field_slot = f"field_slot_{row}_{col}"
                return f"place_{unit_to_place}_{bench_coords[0]}_{bench_coords[1]}_{field_slot}"
        return None
