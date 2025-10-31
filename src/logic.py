from config import BENCH_SIZE

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
        # Placeholder for merge logic
        # In a real scenario, this would check the bench and field for two of the same unit
        # and return a "merge" action if a pair is found.
        return None
