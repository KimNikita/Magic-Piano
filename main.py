import logging as log
import os
import sys
import cv2
from screeninfo import get_monitors
from piano import Piano
from piano_key import PianoKey
from hand_tracking import HandDetector


def main():
    log.basicConfig(format='[ %(levelname)s ] %(message)s',
                    level=log.INFO, stream=sys.stdout)


# инициализация значений
cap = cv2.VideoCapture(0)
detector = HandDetector()
monitor = get_monitors()

# генерация клавиш и пианино
# piano = Piano(100,100,200,200)

# работа нейросети
while cap.isOpened():
    success, img = cap.read()
    img = cv2.resize(img, (int(monitor[0].width/2), int(monitor[0].height/2)),
                     interpolation=cv2.INTER_AREA)
    hand_points = detector.findPosition(img, True)

    # обрабатываем выход сети

    # отрисовка
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if __name__ == '__main__':
    sys.exit(main() or 0)
