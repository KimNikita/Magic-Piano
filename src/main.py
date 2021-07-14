import logging as log
import os
import sys
sys.path.append("..")
import cv2 as cv
from screeninfo import get_monitors
from modules.piano import Piano
from modules.piano_key import PianoKey
from modules.hand_tracking import HandDetector


def main():
    log.basicConfig(format='[ %(levelname)s ] %(message)s',
                    level=log.INFO, stream=sys.stdout)

    # инициализация значений
    cap = cv.VideoCapture(0)
    detector = HandDetector()
    monitor = get_monitors()

    # генерация клавиш и пианино
    # piano = Piano(100,100,200,200)

    # работа нейросети
    while cap.isOpened():
        success, img = cap.read()
        img = cv.flip(img, 1)
        img = cv.resize(img, (int(monitor[0].width/2), int(monitor[0].height/2)),
                        interpolation=cv.INTER_AREA)
        hand_points = detector.findPosition(img, True)

        # обрабатываем выход сети

        # отрисовка
        cv.imshow("Image", img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    sys.exit(main() or 0)
