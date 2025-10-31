import pygetwindow as gw
import subprocess
import os

class ProcessManager:
    def __init__(self, window_name="Bluestacks", executable_path=None):
        self.window_name = window_name
        self.executable_path = executable_path or self.find_bluestacks_path()

    def find_bluestacks_path(self):
        # Common installation paths for BlueStacks
        program_files = os.environ.get("ProgramFiles", "C:\\Program Files")
        possible_paths = [
            os.path.join(program_files, "BlueStacks_nxt", "HD-Player.exe"),
            os.path.join(program_files, "BlueStacks", "HD-Player.exe"),
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def is_running(self):
        return len(gw.getWindowsWithTitle(self.window_name)) > 0

    def start_process(self):
        if self.executable_path and not self.is_running():
            print("BlueStacks not found. Starting...")
            try:
                subprocess.Popen([self.executable_path])
                print("BlueStacks started.")
            except Exception as e:
                print(f"Failed to start BlueStacks: {e}")
        elif not self.executable_path:
            print("BlueStacks executable not found.")
