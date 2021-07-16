from modules.piano import Piano
from screeninfo import get_monitors
import time
import os
import cv2 as cv
import sys
sys.path.append("..")


def main():
    cap = cv.VideoCapture(0)
    monitor = get_monitors()
    spath = os.path.abspath('')[:-7] + '\\sounds\\sound_4'
    piano = Piano(0, 0, int(monitor[0].width/2), int(monitor[0].height/4))
    piano.generator_7(spath)

    for i in range(7):
        success, img = cap.read()
        img = cv.flip(img, 1)
        img = cv.resize(img, (int(monitor[0].width/2), int(monitor[0].height/2)),
                        interpolation=cv.INTER_AREA)

        piano.keys[i].press()
        img = piano.draw(img)
        cv.imshow("Image", img)
        time.sleep(0.8)
        piano.keys[i].unpress()
        if cv.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    sys.exit(main() or 0)
