from screeninfo import get_monitors
import cv2 as cv
import math
import os
import sys

sys.path.append("..")

from PySide2 import QtCore, QtGui, QtWidgets
import qimage2ndarray

from modules.hand_tracking import HandDetector
from modules.piano_key import PianoKey
from modules.piano import Piano

monitor = get_monitors()

m_width = monitor[0].width
m_height = monitor[0].height

detector = HandDetector()

# генерация клавиш и пианино
piano = Piano(int(m_width / 50), int(m_height / 50),
              int(m_width / 1.6), int(m_height / 3))
spath = os.path.abspath('')[:-7] + '\\sounds'
piano.key_generator(spath, 4, 7)

turn = 1
cond = 20
pianolen = len(piano.keys)
indent = int(m_width / 50)


class VideoPlayer(QtWidgets.QWidget):
    pause = False
    video = False

    def __init__(self, fps=30):
        QtWidgets.QWidget.__init__(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle('Magic Piano')
        self.setFixedSize(self.sizeHint())
        self.camera_capture = cv.VideoCapture(cv.CAP_DSHOW)
        self.video_capture = cv.VideoCapture()

        self.frame_timer = QtCore.QTimer()
        self.setup_camera(fps)

        self.fps = fps

        # в Qt label работает для вывода изображения
        self.frame_label = QtWidgets.QLabel()
        self.quit_buttom = QtWidgets.QPushButton('Quit')
        self.play_pause_buttom = QtWidgets.QPushButton('Pause')
        self.camera_video_buttom = QtWidgets.QPushButton('Switch to video')

        self.main_layout = QtWidgets.QGridLayout()

        self.setup_ui()

        self.play_pause_buttom.clicked.connect(self.play_pause)
        self.camera_video_buttom.clicked.connect(self.camera_video)

    def setup_ui(self):
        # передали адрес функции
        self.quit_buttom.clicked.connect(self.close_win)

        # геолокация 1-2 клеточки 1-размер по высоте 2-по ширине
        self.main_layout.addWidget(self.frame_label, 0, 0, 1, 2)
        self.main_layout.addWidget(self.play_pause_buttom, 1, 0, 1, 1)
        self.main_layout.addWidget(self.camera_video_buttom, 1, 1, 1, 1)
        self.main_layout.addWidget(self.quit_buttom, 2, 0, 1, 2)

        self.setLayout(self.main_layout)

    def play_pause(self):
        if not self.pause:
            self.frame_timer.stop()
            self.play_pause_buttom.setText('Play')
        else:
            self.frame_timer.start(int(1000 // self.fps))
            self.play_pause_buttom.setText('Pause')
        self.pause = not self.pause

    def camera_video(self):
        if not self.video:
            path = QtWidgets.QFileDialog.getOpenFileName(dir='C:\\', filter='Videos (*.mp4)')
            if len(path[0]):
                self.video_capture.open(path[0])
                self.camera_video_buttom.setText('Switch to camera')
            else:
                self.camera_video_buttom.setText('Switch to video')
                self.video_capture.release()

        self.video = not self.video

    def setup_camera(self, fps):
        self.frame_timer.timeout.connect(self.display_video_stream)
        # timer (msec)
        self.frame_timer.start(int(1000 // fps))

    def display_video_stream(self):

        if not self.video:
            ret, img = self.camera_capture.read()
        else:
            ret, img = self.video_capture.read()

        if not ret:
            return False

        if not self.video:
            img = cv.flip(img, turn)

        img = cv.resize(img, (int(m_width / 1.5), int(m_height / 1.5)),
                        interpolation=cv.INTER_AREA)
        left_points, right_points = detector.findPosition(img, True)
        fingers = []
        zone = piano.keys[0].height
        hashs = piano.keys[0].width
        pressed = {}
        for key in piano.keys:
            pressed[key] = False

        if left_points:
            for i in range(len(left_points)):
                if left_points[i][2] < zone and left_points[i][0] % 4 == 0:
                    fingers.append((left_points[i], left_points[i - 1]))
        if right_points:
            for i in range(len(right_points)):
                if right_points[i][2] < zone and right_points[i][0] % 4 == 0:
                    fingers.append((right_points[i], right_points[i - 1]))
        if fingers:
            for finger in fingers:
                key_hash = (finger[0][1] - indent -
                            (finger[0][1] // hashs) * piano.indent) // hashs
                if -1 < key_hash < pianolen:
                    if finger[0][2] > finger[1][2] or math.sqrt(
                            (finger[0][1] - finger[1][1]) ** 2 + (finger[0][2] - finger[1][2]) ** 2) < cond:
                        piano.keys[key_hash].press()
                        pressed[key_hash] = True

        for key in piano.keys:
            if not pressed[key]:
                piano.keys[key].unpress()
        # отрисовка
        img = piano.draw(img)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        image = qimage2ndarray.array2qimage(img)

        self.frame_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def close_win(self):
        cv.destroyAllWindows()
        self.camera_capture.release()
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    player = VideoPlayer()
    player.show()

    sys.exit(app.exec_())
