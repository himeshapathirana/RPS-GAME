import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


class UIComponents:
    def __init__(self, font_path=None):
        self.font_path = font_path
        self.font_available = self._check_font_available()

    def _check_font_available(self):
        try:
            if self.font_path:
                ImageFont.truetype(self.font_path, 30)
                return True
        except:
            return False
        return False

    def draw_text_with_outline(self, img, text, position, font_scale, color, thickness, outline_color,
                               outline_thickness):
        if self.font_available:
            img_pil = Image.fromarray(img)
            draw = ImageDraw.Draw(img_pil)
            font_size = int(img.shape[0] * font_scale / 20)
            try:
                font = ImageFont.truetype(self.font_path, font_size)
            except:
                font = ImageFont.load_default()

            x, y = position

            for x_offset in [-outline_thickness, 0, outline_thickness]:
                for y_offset in [-outline_thickness, 0, outline_thickness]:
                    if x_offset != 0 or y_offset != 0:
                        draw.text((x + x_offset, y + y_offset), text, font=font, fill=outline_color)

            draw.text((x, y), text, font=font, fill=color)
            img[:] = np.array(img_pil)
        else:
            x, y = position
            cv2.putText(img, text, (x - outline_thickness, y), cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale, outline_color, outline_thickness * 2)
            cv2.putText(img, text, (x, y - outline_thickness), cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale, outline_color, outline_thickness * 2)
            cv2.putText(img, text, (x + outline_thickness, y), cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale, outline_color, outline_thickness * 2)
            cv2.putText(img, text, (x, y + outline_thickness), cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale, outline_color, outline_thickness * 2)
            cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale, color, thickness)

    def draw_scoreboard(self, img, score, round_count, max_rounds):
        cv2.rectangle(img, (20, 20), (250, 120), (50, 50, 50), -1)
        cv2.rectangle(img, (20, 20), (250, 120), (212, 175, 55), 2)

        self.draw_text_with_outline(img, f"Score: {score}", (30, 50),
                                    0.8, (255, 255, 255), 2, (0, 0, 0), 1)
        self.draw_text_with_outline(img, f"Round: {round_count}/{max_rounds}", (30, 80),
                                    0.8, (255, 255, 255), 2, (0, 0, 0), 1)
        self.draw_text_with_outline(img, f"Total: {max_rounds}", (30, 110),
                                    0.8, (255, 255, 255), 2, (0, 0, 0), 1)

    def draw_versus(self, img):
        self.draw_text_with_outline(img, "VS", (img.shape[1] // 2 - 30, img.shape[0] // 2 + 50),
                                    1.5, (255, 0, 255), 5, (0, 0, 0), 2)

    def draw_button(self, img, x, y, width, height, color, text, text_color=(0, 0, 0)):
        cv2.rectangle(img, (x, y), (x + width, y + height), color, -1)
        cv2.rectangle(img, (x, y), (x + width, y + height), (0, 0, 0), 2)
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        text_x = x + (width - text_size[0]) // 2
        text_y = y + (height + text_size[1]) // 2
        self.draw_text_with_outline(img, text, (text_x, text_y), 0.8, text_color, 2, (255, 255, 255), 1)