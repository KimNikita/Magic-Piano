from modules.hand_tracking import HandDetector
from modules.piano_key import PianoKey
from modules.piano import Piano
from screeninfo import get_monitors
import cv2 as cv
import logging as log
import os
import math
import sys
sys.path.append("..")


def main():
    log.basicConfig(format='[ %(levelname)s ] %(message)s',
                    level=log.INFO, stream=sys.stdout)

    # инициализация значений
    cap = cv.VideoCapture(0)
    detector = HandDetector()
    monitor = get_monitors()
    m_width = monitor[0].width
    m_height = monitor[0].height

    # генерация клавиш и пианино
    piano = Piano(0, 0, int(m_width/1.5), int(m_height/3))
    spath = os.path.abspath('') + 'sounds\sound_7'
    piano.generator_7(spath)

    # работа нейросети
    while cap.isOpened():
        success, img = cap.read()
        img = cv.flip(img, 1)
        img = cv.resize(img, (int(m_width/1.5), int(m_height/1.5)),
                        interpolation=cv.INTER_AREA)
        left_points, right_points = detector.findPosition(img, True)
        cond = 25
        for key in piano.keys:
            f = False
            if left_points:
                for point2 in left_points:
                    if point2[0] in {4, 8, 12, 16, 20}:
                        if key.middle[1] >= point2[2] and point2[1] < key.right[0] and point2[1] > key.left[0]:
                            for point1 in left_points:
                                if point1[0] == point2[0]-1:
                                    if math.sqrt((point2[1]-point1[1])**2 + (point2[2]-point1[2])**2) < cond:
                                        key.press()
                                        f = True
                                        break

            if f == False:
                if right_points:
                    for point2 in right_points:
                        if point2[0] in {4, 8, 12, 16, 20}:
                            if key.middle[1] >= point2[2] and point2[1] < key.right[0] and point2[1] > key.left[0]:
                                for point1 in right_points:
                                    if point1[0] == point2[0]-1:
                                        if math.sqrt((point2[1]-point1[1])**2 + (point2[2]-point1[2])**2) < cond:
                                            key.press()
                                            f = True
                                            break

                if f == False:
                    key.unpress()

        # отрисовка
        img = piano.draw(img)
        cv.imshow("Image", img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    sys.exit(main() or 0)
