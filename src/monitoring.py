import time
import datetime
import os

class Monitor:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f"log_{datetime.date.today()}.txt")

        self.start_time = time.time()
        self.frames_processed = 0
        self.wins = 0
        self.losses = 0

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

    def record_frame(self):
        self.frames_processed += 1

    def record_win(self):
        self.wins += 1
        self.log("Game won!")

    def record_loss(self):
        self.losses += 1
        self.log("Game lost!")

    def get_fps(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time == 0:
            return 0
        return self.frames_processed / elapsed_time

    def get_win_rate(self):
        total_games = self.wins + self.losses
        if total_games == 0:
            return 0
        return self.wins / total_games

    def print_stats(self):
        stats = f"""
        --------------------
        Session Stats:
        Duration: {datetime.timedelta(seconds=int(time.time() - self.start_time))}
        FPS: {self.get_fps():.2f}
        Wins: {self.wins}
        Losses: {self.losses}
        Win Rate: {self.get_win_rate():.2%}
        --------------------
        """
        print(stats)
        self.log(stats)
