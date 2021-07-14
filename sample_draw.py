import sys
import cv2
from screeninfo import get_monitors
from piano import Piano


def main():
    cap = cv2.VideoCapture(0)
    monitor = get_monitors()

    piano = Piano(0, 0, int(monitor[0].width/2), int(monitor[0].height/4))
    piano.generator_7()

    while cap.isOpened():
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (int(monitor[0].width/2), int(monitor[0].height/2)),
                         interpolation=cv2.INTER_AREA)

        img = piano.draw(img)

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    sys.exit(main() or 0)
