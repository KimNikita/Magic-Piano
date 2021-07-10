import sys
import os
import numpy as np


class Piano:
    self.left = None
    self.right = None
    self.keys = []

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

    def draw(self):
        for key in self.keys:
            # рисуем клавишу
            pass
