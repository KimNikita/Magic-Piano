import time
import os
import numpy as np
import cv2 as cv
import sys
sys.path.append("..")
from modules.piano import Piano
from screeninfo import get_monitors

def main():
    cap = cv.VideoCapture(0)
    monitor = get_monitors()
    spath = os.path.abspath('')[:-7] + '\\sounds'
    piano = Piano(0, 0, int(monitor[0].width/2), int(monitor[0].height/4))
    piano.key_generator(spath, 3, 7)
    cam = False
    if cam:
        success, img = cap.read()
        img = cv.resize(img, (int(monitor[0].width/2), int(monitor[0].height/2)),
                        interpolation=cv.INTER_AREA)
    else:
        img = np.random.randint(255, size=(
            int(monitor[0].height/2), int(monitor[0].width/2), 3), dtype=np.uint8)
    img = piano.draw(img)

    for i in range(7):
        piano.press_key(i)
        img = piano.draw(img)

        cv.imshow("Image", img)
        time.sleep(0.8)

        piano.unpress_key(i)
        img = piano.draw(img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    sys.exit(main() or 0)
