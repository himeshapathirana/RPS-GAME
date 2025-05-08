import random
import time


class GameState:
    def __init__(self):
        self.game_active = False
        self.player_choice = ""
        self.computer_choice = ""
        self.result = ""
        self.score = 0
        self.round_count = 0
        self.last_gesture_time = 0
        self.countdown = 3  # Countdown before player shows gesture
        self.last_countdown_time = 0
        self.game_start_time = 0
        self.start_screen_time = 0
        self.show_result = False
        self.result_display_start = 0
        self.waiting_for_gesture = False
        self.round_active = False
        self.fullscreen = False
        self.show_final_screen = False
        self.final_screen_start_time = 0

    def reset_round(self):
        self.player_choice = ""
        self.computer_choice = ""
        self.result = ""
        self.countdown = 3
        self.last_countdown_time = time.time()
        self.waiting_for_gesture = False
        self.round_active = True
        self.show_result = False

    def start_new_game(self):
        self.game_active = True
        self.score = 0
        self.round_count = 0
        self.game_start_time = time.time()
        self.reset_round()

    def get_computer_choice(self):
        choices = ["Rock", "Paper", "Scissors"]
        return random.choice(choices)

    def determine_winner(self, player, computer):
        if player == computer:
            return "Draw!", (0, 255, 255)  # Yellow
        if (player == "Rock" and computer == "Scissors") or \
                (player == "Paper" and computer == "Rock") or \
                (player == "Scissors" and computer == "Paper"):
            return "You Win!", (0, 255, 0)  # Green
        return "Computer Wins!", (0, 0, 255)  # Red