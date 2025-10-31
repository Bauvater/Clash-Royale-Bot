import pyautogui

class GameController:
    def __init__(self, window_rect):
        self.window_rect = window_rect

    def _get_absolute_coords(self, x, y):
        return self.window_rect["left"] + x, self.window_rect["top"] + y

    def click(self, x, y):
        abs_x, abs_y = self._get_absolute_coords(x, y)
        pyautogui.click(abs_x, abs_y)

    def drag(self, start_x, start_y, end_x, end_y, duration=0.5):
        start_abs_x, start_abs_y = self._get_absolute_coords(start_x, start_y)
        end_abs_x, end_abs_y = self._get_absolute_coords(end_x, end_y)
        pyautogui.moveTo(start_abs_x, start_abs_y)
        pyautogui.dragTo(end_abs_x, end_abs_y, duration=duration)
