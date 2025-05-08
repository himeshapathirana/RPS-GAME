import cv2
import time


class StartPage:
    def __init__(self, ui_components):
        self.ui = ui_components
        self.start_screen_time = 0

    def show(self, img_bg, current_time):
        if self.start_screen_time == 0:
            self.start_screen_time = current_time

        time_remaining = max(0, 3 - (current_time - self.start_screen_time))
        self.ui.draw_text_with_outline(img_bg, f"Starting in: {int(time_remaining) + 1}",
                                       (img_bg.shape[1] // 2 - 150, img_bg.shape[0] - 100),
                                       1.2, (255, 255, 255), 3, (0, 0, 0), 2)

        self.ui.draw_text_with_outline(img_bg, "Rock Paper Scissors",
                                       (img_bg.shape[1] // 2 - 200, 150),
                                       1.5, (212, 175, 55), 5, (0, 0, 0), 3)

        if current_time - self.start_screen_time > 3:
            self.start_screen_time = 0
            return True
        return False