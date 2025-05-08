import cv2
import time


class GamePage:
    def __init__(self, ui_components, hand_detector, image_loader):
        self.ui = ui_components
        self.hand_detector = hand_detector
        self.image_loader = image_loader
        self.symbols = {
            "Rock": None,
            "Paper": None,
            "Scissors": None,
            "Thinking": None
        }

    def load_symbols(self):
        # Load all game symbols
        self.symbols["Rock"] = self.image_loader.load_image("Resources/rock.jpg")
        self.symbols["Paper"] = self.image_loader.load_image("Resources/paper.jpg")
        self.symbols["Scissors"] = self.image_loader.load_image("Resources/scissors.jpg")
        self.symbols["Thinking"] = self.image_loader.load_image("Resources/thinking.png", True)

        # Resize all symbols
        for key in self.symbols:
            if self.symbols[key] is not None:
                self.symbols[key] = self.image_loader.resize_image(self.symbols[key], 312, 360)

    def process_frame(self, img_bg, img_webcam, game_state):
        current_time = time.time()  # Define current_time at the start

        # Draw game elements
        self.ui.draw_scoreboard(img_bg, game_state.score, game_state.round_count, 5)

        # Draw computer's box
        cv2.rectangle(img_bg, (100, 280), (412, 640), (212, 175, 55), 2)

        # Draw player's box
        cv2.rectangle(img_bg, (878, 280), (1190, 640), (212, 175, 55), 2)

        if game_state.round_active:
            if game_state.countdown > 0:
                if current_time - game_state.last_countdown_time > 1:
                    game_state.countdown -= 1
                    game_state.last_countdown_time = current_time

                countdown_size = 1 + (3 - game_state.countdown) * 0.2
                self.ui.draw_text_with_outline(img_bg, str(game_state.countdown),
                                               (img_bg.shape[1] // 2 - 30, img_bg.shape[0] // 2),
                                               countdown_size, (255, 255, 255), 8, (0, 0, 0), 3)

                self.ui.draw_text_with_outline(img_bg, "Get Ready!",
                                               (img_bg.shape[1] // 2 - 120, img_bg.shape[0] // 2 - 100),
                                               1.2, (0, 255, 255), 3, (0, 0, 0), 2)

                if self.symbols["Thinking"] is not None:
                    self.image_loader.overlay_image(img_bg, self.symbols["Thinking"], [100, 280])
            else:
                game_state.waiting_for_gesture = True
                self.ui.draw_text_with_outline(img_bg, "Show Your Move!",
                                               (img_bg.shape[1] // 2 - 150, img_bg.shape[0] // 2 - 100),
                                               1.2, (0, 255, 0), 3, (0, 0, 0), 2)

                player_choice = self.hand_detector.detect_gesture(img_webcam)
                if player_choice and game_state.waiting_for_gesture:
                    game_state.player_choice = player_choice
                    game_state.computer_choice = game_state.get_computer_choice()
                    game_state.result, _ = game_state.determine_winner(game_state.player_choice,
                                                                       game_state.computer_choice)

                    if "Win" in game_state.result and "You" in game_state.result:
                        game_state.score += 1

                    game_state.round_count += 1
                    game_state.show_result = True
                    game_state.result_display_start = current_time
                    game_state.round_active = False

        if game_state.computer_choice and self.symbols[game_state.computer_choice] is not None:
            self.image_loader.overlay_image(img_bg, self.symbols[game_state.computer_choice], [100, 280])

        self.ui.draw_versus(img_bg)

        if game_state.show_result:
            result_text, result_color = game_state.determine_winner(game_state.player_choice,
                                                                    game_state.computer_choice)
            self.ui.draw_text_with_outline(img_bg, result_text,
                                           (img_bg.shape[1] // 2 - 120, 150),
                                           1.5, result_color, 5, (0, 0, 0), 3)

            if current_time - game_state.result_display_start > 2:
                game_state.show_result = False
                if game_state.round_count < 5:
                    game_state.reset_round()
                else:
                    return "game_over"

        # Process webcam feed
        scale = 360 / img_webcam.shape[0]
        image_scaled = cv2.resize(img_webcam, (0, 0), fx=scale, fy=scale)
        center_x = image_scaled.shape[1] // 2
        image_cropped = image_scaled[:, center_x - 156:center_x + 156]
        image_cropped = cv2.resize(image_cropped, (312, 360))

        border_size = 5
        border_color = (0, 255, 0) if game_state.player_choice else (212, 175, 55)
        image_cropped = cv2.copyMakeBorder(
            image_cropped,
            border_size, border_size, border_size, border_size,
            cv2.BORDER_CONSTANT,
            value=border_color
        )

        try:
            img_bg[280 - border_size:280 + 360 + border_size,
            878 - border_size:878 + 312 + border_size] = image_cropped
        except ValueError:
            target_height = 280 + 360 + border_size - (280 - border_size)
            target_width = 878 + 312 + border_size - (878 - border_size)
            image_cropped = cv2.resize(image_cropped, (target_width, target_height))
            img_bg[280 - border_size:280 + 360 + border_size,
            878 - border_size:878 + 312 + border_size] = image_cropped

        return "continue"