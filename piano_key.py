import sys
import os
import numpy as np


class PianoKey():
    # note - нота (пример "E1"), sound - путь до звукового файла
    # x1 x2 y1 y2 - координаты в пикселях если не переданы размеры image, иначе - координаты в зависимости от размеров image
    def __init__(self, x1, y1, x2, y2, note, sound, image_height=None, image_width=None):
        if image_height:
            self.left = (x1 * image_width, y1 * image_height)
            self.right = (x2 * image_width, y2 * image_height)
        else:
            self.left = (x1, y1)
            self.right = (x2, y2)
        self.height = y2-y1
        self.width = x2-x1
        self.note = note
        self.sound = sound
        self.middle = (x2-x1, y2-y1)
        self.pressed = False
        self.color = (255, 255, 255)

    def play_sound(self):
        pass

    def postprocessing(self, out):
        # Gain - фильтр, выход нейросети, восстанавливает амплитуду речи
        Gain = np.transpose(out)

        # обрезаем значения, поскольку мы стремимся только к уменьшению аддитивного шума a_max=1.0
        Gain = np.clip(Gain, a_min=self.mingain, a_max=1.0)
        # print('filter')
        # print(Gain.shape)

        # применяя фильтр к входному спектру (образ Фурье), избавляемся от шума
        outSpec = np.expand_dims(self.inputSpec, axis=2) * Gain
        # print('denoised_spec')

        # преобразуем обратно в массив амплитуд звукового сигнала
        out = spec2sig(outSpec, self.cfg)
        # print('denoised_audio')
        # print(out.shape)

        return out

    def denoise(self, data):
        # получаем спектр мощности для входа нейросети
        inputFeature = self.preprocessing(data)

        # Calculate network output
        out = self.exec_net.infer({self.input_blob: inputFeature})[
            self.output_blob]

        # обрабатываем выход нейросети (фильтр) и конвертируем выходной спектр в звук
        result = self.postprocessing(out)

        return result
