class EndPage:
    def __init__(self, ui_components):
        self.ui = ui_components

    def show(self, img_bg, score):
        self.ui.draw_text_with_outline(img_bg, f"Final Score: {score}",
                                       (img_bg.shape[1] // 2 - 120, 450),
                                       1.5, (255, 255, 255), 3, (0, 0, 0), 2)

        self.ui.draw_text_with_outline(img_bg, "Play Again?",
                                       (img_bg.shape[1] // 2 - 100, 500),
                                       1.5, (212, 175, 55), 3, (0, 0, 0), 2)

        self.ui.draw_button(img_bg, img_bg.shape[1] // 2 - 150, 550, 100, 50,
                            (0, 255, 0), "YES")
        self.ui.draw_button(img_bg, img_bg.shape[1] // 2 + 50, 550, 100, 50,
                            (0, 0, 255), "NO")