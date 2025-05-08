import cv2
import time

from Resources.components.game_state import GameState
from Resources.components.hand_detector import HandDetectorWrapper
from Resources.components.image_utils import ImageLoader
from Resources.components.ui_components import UIComponents
from Resources.pages.end_page import EndPage
from Resources.pages.game_page import GamePage
from Resources.pages.start_page import StartPage


def main():
    # Initialize components
    font_path = "IMFeENsc28P.ttf"
    ui = UIComponents(font_path)
    image_loader = ImageLoader(font_path)
    hand_detector = HandDetectorWrapper()
    game_state = GameState()

    # Initialize pages
    start_page = StartPage(ui)
    game_page = GamePage(ui, hand_detector, image_loader)
    end_page = EndPage(ui)

    # Load game symbols
    game_page.load_symbols()

    # Open webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # Create window
    cv2.namedWindow("Rock Paper Scissors", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Rock Paper Scissors", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and game_state.show_final_screen:
            if (img_bg.shape[1] // 2 - 150 <= x <= img_bg.shape[1] // 2 - 50 and
                    550 <= y <= 600):
                game_state.show_final_screen = False
                game_state.start_screen_time = time.time()
            elif (img_bg.shape[1] // 2 + 50 <= x <= img_bg.shape[1] // 2 + 150 and
                  550 <= y <= 600):
                cap.release()
                cv2.destroyAllWindows()
                exit()

    cv2.setMouseCallback("Rock Paper Scissors", mouse_callback)

    while True:
        # Load background
        img_bg = image_loader.load_image("Resources/Bg.png")
        img_bg = image_loader.resize_image(img_bg, 1280, 720)

        # Read webcam
        success, img = cap.read()
        if not success:
            break
        img = cv2.flip(img, 1)

        if not game_state.game_active:
            if game_state.show_final_screen:
                img_game_over = image_loader.load_image("Resources/game_over.jpg")
                img_bg = image_loader.resize_image(img_game_over, 1280, 720)
                end_page.show(img_bg, game_state.score)

                key = cv2.waitKey(1)
                if key == ord('y') or key == ord('Y'):
                    game_state.show_final_screen = False
                    game_state.start_screen_time = time.time()
                elif key == ord('n') or key == ord('N'):
                    break
            else:
                img_start = image_loader.load_image("Resources/start.png")
                img_bg = image_loader.resize_image(img_start, 1280, 720)
                if start_page.show(img_bg, time.time()):
                    game_state.start_new_game()
        else:
            result = game_page.process_frame(img_bg, img, game_state)
            if result == "game_over":
                game_state.game_active = False
                game_state.show_final_screen = True

        cv2.imshow("Rock Paper Scissors", img_bg)

        if cv2.getWindowProperty("Rock Paper Scissors", cv2.WND_PROP_VISIBLE) < 1:
            break

        key = cv2.waitKey(1)
        if key == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()