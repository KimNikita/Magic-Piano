from modules.piano_key import PianoKey
import numpy as np
import os
import sys

sys.path.append("..")


class Piano:
    left = None
    right = None
    indent = None
    keys = {}
    tstart = None

    def __init__(self, x1, y1, x2, y2, keys=None, image_height=None, image_width=None):
        if image_height:
            self.left = (x1 * image_width, y1 * image_height)
            self.right = (x2 * image_width, y2 * image_height)
        else:
            self.left = (x1, y1)
            self.right = (x2, y2)
        if keys:
            self.keys = keys
        self.indent = 7

    def add_key(self, key):
        self.keys[key.hash] = key

    def draw(self, img):
        for key in self.keys:
            img = self.keys[key].draw_key(img, self.tstart)
        return img

    def press_key(self, id):
        if -1 < id < len(self.keys):
            self.keys[id].press()

    def unpress_key(self, id):
        if -1 < id < len(self.keys):
            self.keys[id].unpress()

    def get_key_shape(self, id):
        if -1 < id < len(self.keys):
            return [self.keys[id].height, self.keys[id].width]

    def key_generator(self, spath, octave, key_num):
        # <!!! ОЧЕНЬ нужная штука !!!> #
        self.keys = {}
        octave_max = 5
        octave_min = 3
        self.tstart = 90/key_num

        if ((octave_max - octave + 1) * 7 < key_num or octave < octave_min):
            octave = octave_min
            key_num = 7

        notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        px1, py1 = self.left
        px2, py2 = self.right
        width = int(((px2 - px1) - self.indent * key_num) / key_num)
        height = py2 - py1
        x = self.left[0]
        y = self.left[1]
        div = key_num // 7
        mod = key_num % 7
        k = 0

        for i in range(div):
            for j in range(7):
                self.keys[k] = PianoKey(x, y, x + width, y + height, notes[j] + str(octave),
                                        spath + '\\sound_' + str(octave))
                x += width + self.indent
                k += 1
            octave += 1

        for i in range(mod):
            self.keys[k] = PianoKey(x, y, x + width, y + height, notes[i] + str(octave),
                                    spath + '\\sound_' + str(octave))
            k += 1
            x += width + self.indent

    def set_settings(self):
        pass
