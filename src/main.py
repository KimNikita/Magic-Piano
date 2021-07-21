from screeninfo import get_monitors
from modules.game_func import Game
import cv2 as cv
import logging as log
import os
import sys

sys.path.append("..")


def balance(id):
    if id == 4:
        return 6
    elif id == 20:
        return -2
    return 0


def main():
    log.basicConfig(format='[ %(levelname)s ] %(message)s',
                    level=log.INFO, stream=sys.stdout)
    spath = os.path.abspath('') + '\\sounds'
    cap = cv.VideoCapture(0)

    monitor = get_monitors()
    m_width = monitor[0].width
    m_height = monitor[0].height
    while cap.isOpened():
        success, img = cap.read()
        height, width = img.shape[:2]
        pgame = Game(height, width, spath)
        img = pgame.render(img)
        img = cv.resize(img, (int(m_width / 1.5), int(m_height / 1.5)),
                        interpolation=cv.INTER_AREA)
        cv.imshow("Image", img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    sys.exit(main() or 0)
