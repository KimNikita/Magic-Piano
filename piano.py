import sys
import os
import numpy as np

class Piano():
    def __init__(self, model, device):
        self.cfg = {
            'winlen': 0.02,
            'hopfrac': 0.5,
            'fs': 16000,
            'mingain': -80,
            'feattype': 'LogPow'
        }

        # минимальные значения для выхода нейросети
        self.mingain = 10**(self.cfg['mingain']/20)

        # Plugin initialization
        ie = IECore()
        net = ie.read_network(model, os.path.splitext(model)[0] + ".bin")
        self.input_blob = next(iter(net.input_info))  # ?
        self.output_blob = 'output'
        assert len(net.input_info) == 1, "One input is expected"

        # Loading model to the plugin
        self.exec_net = ie.load_network(network=net, device_name=device)

    def preprocessing(self, data):
        # получаем спектр (образ Фурье)
        self.inputSpec = calcSpec(data, self.cfg)
        #print("self.inputSpec.shape: ")
        #print(self.inputSpec.shape)

        # получаем логарифмический спектр мощности
        inputFeature = calcFeat(self.inputSpec, self.cfg)
        
        # shape: [batch x time x freq]
        inputFeature = np.expand_dims(np.transpose(inputFeature), axis=0)

        return inputFeature

    def postprocessing(self, out):
        # Gain - фильтр, выход нейросети, восстанавливает амплитуду речи
        Gain = np.transpose(out)
        
        # обрезаем значения, поскольку мы стремимся только к уменьшению аддитивного шума a_max=1.0
        Gain = np.clip(Gain, a_min=self.mingain, a_max=1.0)
        #print('filter')
        #print(Gain.shape)

        # применяя фильтр к входному спектру (образ Фурье), избавляемся от шума
        outSpec = np.expand_dims(self.inputSpec, axis=2) * Gain
        #print('denoised_spec')

        # преобразуем обратно в массив амплитуд звукового сигнала
        out = spec2sig(outSpec, self.cfg)
        #print('denoised_audio')
        #print(out.shape)

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
