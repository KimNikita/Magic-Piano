import sys
import os
import numpy as np
from piano_key import PianoKey


class Piano:
    left = None
    right = None
    keys = []

    # x1 x2 y1 y2 - координаты в пикселях если не переданы размеры image,
    #    иначе - координаты в зависимости от размеров image
    # keys - список клавиш, если нет, то вручную добавлять через метод

    def __init__(self, x1, y1, x2, y2, keys=None, image_height=None, image_width=None):
        if image_height:
            self.left = (x1 * image_width, y1 * image_height)
            self.right = (x2 * image_width, y2 * image_height)
        else:
            self.left = (x1, y1)
            self.right = (x2, y2)
        if keys:
            self.keys = keys

    def add_key(self, key):
        self.keys.append(key)

    def draw(self, img):
        for key in self.keys:
            img = key.draw_key(img)
        return img

    def generator_7(self):
        notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4']
        path = os.path.abspath('sound_7')
        px1, py1 = self.left
        px2, py2 = self.right
        weight = int((px2 - px1)/7)
        height = py2 - py1
        x = 0
        y = 0

        for i in range(7):
            self.keys.append(
                PianoKey(x, y, x+weight, y+height, notes[i], path))
            x += weight
