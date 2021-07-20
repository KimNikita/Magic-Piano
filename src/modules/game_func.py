import os
import sys
import cv2 as cv
import math
from modules.hand_tracking import HandDetector
from modules.piano_key import PianoKey
from modules.piano import Piano
sys.path.append("..")

class Game:
    detector = None
    monitor = None
    success, img = None, None
    height, width = None, None
    piano = None
    spath = None
    turn = None
    cond = 15
    pianolen = None
    indent = None
    pressed = None

    def __init__(self, cap, path, turn=1, octave=3, key_num=14):
        self.turn = turn
        self.detector = HandDetector()
        self.success, self.img = cap.read()
        self.height, self.width = self.img.shape[:2]
        self.piano = Piano(int(self.width / 50), int(self.height / 50),
                      self.width, int(self.height / 2))
        self.spath = path
        self.piano.key_generator(self.spath, octave, key_num)
        self.pianolen = len(self.piano.keys)
        self.indent = int(self.width / 50)
        self.pressed = {}
        for key in self.piano.keys:
            self.pressed[key] = False

    def balance(self, id):
        if id == 4:
            return 6
        elif id == 20:
            return -2
        return 0

    def render(self, img):
        img = cv.flip(img, self.turn)
        left_points, right_points = self.detector.findPosition(img, True)
        fingers = []
        zone = self.piano.get_key_shape(0)[0]
        hashs = self.piano.get_key_shape(0)[1]

        if left_points:
            for i in range(len(left_points)):
                if left_points[i][2] < zone and left_points[i][0] % 4 == 0:
                    fingers.append((left_points[i], left_points[i - 1]))
        if right_points:
            for i in range(len(right_points)):
                if right_points[i][2] < zone and right_points[i][0] % 4 == 0:
                    fingers.append((right_points[i], right_points[i - 1]))

        if fingers:
            for finger in fingers:
                key_hash = (finger[0][1] - self.indent -
                            (finger[0][1] // hashs) * self.piano.indent) // hashs
                if -1 < key_hash < self.pianolen:
                    if finger[0][2] > finger[1][2] or math.sqrt(
                            (finger[0][1] - finger[1][1]) ** 2 + (finger[0][2] - finger[1][2]) ** 2) < self.cond + self.balance(finger[0][0]):
                        self.piano.press_key(key_hash)
                        self.pressed[key_hash] = True

        for key in self.piano.keys:
            if not self.pressed[key]:
                self.piano.unpress_key(key)
            else:
                self.pressed[key] = False

        img = self.piano.draw(img)
        return(img)