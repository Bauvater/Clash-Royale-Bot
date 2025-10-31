from utils import *
from read_region import *
from game import *
from controller import GameController
from logic import Tactics
from gpu import GPU
from ki import KI
from process import ProcessManager
from monitoring import Monitor
from config import WINDOW_NAME
import cv2
import time

class MergeTacticsBot:
    def __init__(self):
        self.monitor = Monitor()
        self.process_manager = ProcessManager(WINDOW_NAME)
        self.process_manager.start_process()
        time.sleep(15) # Wait for BlueStacks to start
        self.game_info = GameInfo()
        self.game_state = GameState()
        self.reader = ReadRegion(**self.game_info.regions)
        self.controller = GameController(get_window_rect(WINDOW_NAME))
        self.ki = KI()
        self.tactics = Tactics(self.game_state, self.game_info, self.ki)
        self.gpu = GPU()

    def run(self):
        try:
            while True:
                # Main bot loop
                try:
                    self.update_game_state()
                    decision = self.tactics.make_decision()
                    if decision:
                        self.perform_action(decision)

                    game_over, win = self.detect_game_over()
                    if game_over:
                        if win:
                            self.monitor.record_win()
                            self.ki.record_game_result(self.tactics.current_strategy, True)
                        else:
                            self.monitor.record_loss()
                            self.ki.record_game_result(self.tactics.current_strategy, False)
                        self.restart_game()

                except RuntimeError as e:
                    self.monitor.log(f"Error: {e}")
                    print(f"Error: {e}")
                    self.process_manager.start_process()
                    time.sleep(15) # Wait for BlueStacks to start
                    continue
        finally:
            self.monitor.print_stats()

    def update_game_state(self):
        self.monitor.record_frame()
        self.game_state.shop_characters = self.reader.read_shop()
        self.game_state.bench_characters = self.reader.read_bench()
        self.game_state.field_characters = self.reader.read_field()
        self.game_state.elixir = self.reader.read_elixir()

    def perform_action(self, action):
        shop_slot_coords = {
            "buy_slot_1": (150, 980),
            "buy_slot_2": (280, 980),
            "buy_slot_3": (410, 980),
        }
        if action in shop_slot_coords:
            x, y = shop_slot_coords[action]
            self.controller.click(x, y)
        elif "merge" in action:
            # Placeholder for merge logic
            pass

        time.sleep(0.5) # Wait for the action to complete

    def detect_game_over(self):
        # Placeholder for game over detection
        # In a real scenario, this would involve reading the screen for a "Victory" or "Defeat" message.
        return False, False

    def restart_game(self):
        # Placeholder for game restart logic
        self.monitor.log("Restarting game...")
        print("Restarting game...")
        # In a real scenario, this would involve clicking the "Play Again" button.
        time.sleep(5)

if __name__ == "__main__":
    bot = MergeTacticsBot()
    bot.run()
