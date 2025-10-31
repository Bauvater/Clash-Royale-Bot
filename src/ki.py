import json

class KI:
    def __init__(self, strategy_file="strategy_performance.json"):
        self.strategy_file = strategy_file
        self.strategies = self.load_strategies()

    def load_strategies(self):
        try:
            with open(self.strategy_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_strategies(self):
        with open(self.strategy_file, "w") as f:
            json.dump(self.strategies, f, indent=4)

    def record_game_result(self, strategy_name, win):
        if strategy_name not in self.strategies:
            self.strategies[strategy_name] = {"wins": 0, "losses": 0}

        if win:
            self.strategies[strategy_name]["wins"] += 1
        else:
            self.strategies[strategy_name]["losses"] += 1

        self.save_strategies()

    def get_best_strategy(self):
        if not self.strategies:
            return None

        best_strategy = None
        best_win_rate = -1

        for name, stats in self.strategies.items():
            total_games = stats["wins"] + stats["losses"]
            if total_games == 0:
                continue

            win_rate = stats["wins"] / total_games
            if win_rate > best_win_rate:
                best_win_rate = win_rate
                best_strategy = name

        return best_strategy
