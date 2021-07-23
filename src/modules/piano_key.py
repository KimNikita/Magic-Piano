import sys
import os
import numpy as np
import cv2 as cv
from playsound import playsound


class PianoKey:
    left = None
    right = None
    height = None
    width = None
    note = None
    sound = None
    middle = None
    pressed = None
    color = None
    hashkey = None

    def __init__(self, x1, y1, x2, y2, note, sound, image_height=None, image_width=None):
        if image_height:
            self.left = (x1 * image_width, y1 * image_height)
            self.right = (x2 * image_width, y2 * image_height)
            self.height = (y2 - y1) * image_height
            self.width = (x2 - x1) * image_width
        else:
            self.left = (x1, y1)
            self.right = (x2, y2)
            self.height = y2 - y1
            self.width = x2 - x1
        self.hashkey = (x1 + 1) // self.width
        self.note = note
        self.sound = sound
        self.middle = (int((x2 - x1)) / 2, int((y2 - y1) / 2))
        self.pressed = False
        self.color = (255, 255, 255)  # format BGR

    def play_sound(self):
        path = self.sound + '\\' + self.note + '.wav'
        playsound(path, False)

    def press(self):
        if self.pressed:
            return
        else:
            self.play_sound()
            self.color = (255, 0, 0)
            self.pressed = True

    def unpress(self):
        self.pressed = False
        self.color = (255, 255, 255)

    def draw_key(self, img, tstart):
        x, y = self.left
        cv.rectangle(img, self.left, self.right, self.color, cv.LINE_4)
        font = cv.FONT_HERSHEY_PLAIN
        color = (0, 255, 0)
        cv.putText(img, self.note, (x + int(tstart), int(y + self.height * 0.2)),
                   font, int(self.width * 0.046), color, 2)
        #cv.putText(img, text, (x + int(tstart), int(y + self.height * 0.4)),
         #          font, int(self.width * 0.046), color, 2)
        return img
