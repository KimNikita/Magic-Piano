import logging as log
import os
import sys
from piano import Piano
from piano_key import PianoKey


def main():
    log.basicConfig(format='[ %(levelname)s ] %(message)s',
                    level=log.INFO, stream=sys.stdout)

# Примерный pipeline (как я представляю):

# инициализация значений

# работа нейросети
# берем выход сети, смотрим какие пальцы закрыли центры каких клавиш, проигрываем звук,
# изменяем цвет клавиши в зависимости от происходящего

# отрисовка


if __name__ == '__main__':
    sys.exit(main() or 0)
