from modules.hand_tracking import HandDetector
from modules.piano_key import PianoKey
from modules.piano import Piano
import os
import sys
import cv2 as cv
import math

sys.path.append("..")


class Game:
    detector = None
    monitor = None
    success, img = None, None
    piano = None
    spath = None
    turn = None
    cond = 15
    pianolen = None
    indent = None
    hold = None
    time_codes = {}

    def __init__(self, height, width, path, turn = 1, octave = 3, key_num = 7, tpath=None):
        self.turn = turn
        self.detector = HandDetector()
        if tpath:
            self.time_codes = {}
            with open(tpath, 'r') as p:
                times = p.read().split('\n')
            i = 0
            for time in times:
                codes = time.split(' ')
                self.time_codes[i] = codes[1:]
                i += 1
        self.piano = Piano(int(width / 50), int(height / 50),
                           width, int(height / 2))
        self.spath = path
        self.piano.key_generator(self.spath, octave, key_num)
        self.pianolen = len(self.piano.keys)
        self.indent = int(width / 50)
        self.hold = {}
        for key in self.piano.keys:
            self.hold[key] = [False, False]

    def balance(self, id):
        if id == 4:
            return 6
        elif id == 20:
            return -2
        return 0

    def render(self, img, time, debug_mode=True):
        miss = 0
        ismiss = True
        maxtime = time + 0.2
        mintime = time - 0.1
        img = cv.flip(img, self.turn)
        left_points, right_points = self.detector.findPosition(img, debug_mode)
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
                            (finger[0][1] - finger[1][1]) ** 2 + (
                                finger[0][2] - finger[1][2]) ** 2) < self.cond + self.balance(finger[0][0]):
                        self.piano.press_key(key_hash)
                        self.hold[key_hash][1] = True
                        if self.hold[key_hash][0] == False:
                            if self.time_codes:
                                for code in self.time_codes[key_hash]:
                                    if code == '':
                                        break
                                    if mintime < float(code) < maxtime:
                                        ismiss = False
                                if ismiss:
                                    miss += 1
                                else:
                                    ismiss = True

        for key in self.piano.keys:
            if self.hold[key][0] and not self.hold[key][1]:
                self.hold[key][0] = False
                self.piano.unpress_key(key)
            elif not self.hold[key][0] and self.hold[key][1]:
                self.hold[key][0] = True
                self.hold[key][1] = False
            elif not self.hold[key][0] and not self.hold[key][1]:
                self.piano.unpress_key(key)
            else:
                self.hold[key][1] = False



        img = self.piano.draw(img)
        return img, miss
