import cvzone
from cvzone.HandTrackingModule import HandDetector


class HandDetectorWrapper:
    def __init__(self):
        self.detector = HandDetector(maxHands=1, detectionCon=0.8)

    def detect_gesture(self, img):
        hands, img = self.detector.findHands(img, draw=True)
        if hands:
            hand = hands[0]
            fingers = self.detector.fingersUp(hand)

            if fingers == [0, 0, 0, 0, 0]:
                return "Rock"
            elif fingers == [1, 1, 1, 1, 1]:
                return "Paper"
            elif fingers == [0, 1, 1, 0, 0]:
                return "Scissors"
        return None