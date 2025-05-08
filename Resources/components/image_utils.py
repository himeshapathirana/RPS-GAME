import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


class ImageLoader:
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

    def load_image(self, path, with_alpha=False):
        if with_alpha:
            img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        else:
            img = cv2.imread(path)

        if img is None:
            print(f"Error: Could not load image at {path}")
            blank_img = np.zeros((360, 312, 4 if with_alpha else 3), dtype=np.uint8)
            if self.font_available:
                img_pil = Image.fromarray(blank_img)
                draw = ImageDraw.Draw(img_pil)
                font = ImageFont.truetype(self.font_path, 30)
                draw.text((50, 180), "Image Missing", font=font, fill=(255, 255, 255))
                blank_img = np.array(img_pil)
            else:
                cv2.putText(blank_img, "Image Missing", (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            return blank_img
        return img

    def resize_image(self, img, width, height):
        return cv2.resize(img, (width, height))

    def overlay_image(self, bg_img, fg_img, pos):
        x, y = pos
        h, w = fg_img.shape[:2]

        if x < 0 or y < 0 or x + w > bg_img.shape[1] or y + h > bg_img.shape[0]:
            print(f"Warning: Image at position {pos} would be out of bounds")
            return bg_img

        if fg_img.shape[2] == 4:
            alpha = fg_img[:, :, 3] / 255.0
            inv_alpha = 1 - alpha
            for c in range(0, 3):
                bg_img[y:y + h, x:x + w, c] = (alpha * fg_img[:, :, c] +
                                               inv_alpha * bg_img[y:y + h, x:x + w, c])
        else:
            bg_img[y:y + h, x:x + w] = fg_img
        return bg_img