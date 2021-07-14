import sys
sys.path.append("..")
import cv2 as cv
from screeninfo import get_monitors
from modules.piano import Piano


def main():
    cap = cv.VideoCapture(0)
    monitor = get_monitors()

    piano = Piano(0, 0, int(monitor[0].width/2), int(monitor[0].height/4))
    piano.generator_7()

    while cap.isOpened():
        success, img = cap.read()
        img = cv.flip(img, 1)
        img = cv.resize(img, (int(monitor[0].width/2), int(monitor[0].height/2)),
                        interpolation=cv.INTER_AREA)

        img = piano.draw(img)

        cv.imshow("Image", img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    sys.exit(main() or 0)
