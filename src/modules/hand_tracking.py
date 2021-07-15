import mediapipe as mp
import cv2 as cv


class HandDetector:
    mode = None
    maxHands = None
    decectionCon = None
    trackCon = None
    mpHands = None
    hands = None
    mpDraw = None

    def __init__(self, mode=False, maxHands=2, decectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = decectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findPosition(self, img, draw=False):
        l_list = []
        r_list = []
        f = 0
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    if not f:
                        l_list.append([id, cx, cy])
                    else:
                        r_list.append([id, cx, cy])
                f = 1
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)
        return l_list, r_list
