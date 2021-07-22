from screeninfo import get_monitors
import cv2 as cv
import math
import os
import sys
import numpy as np

sys.path.append("..")

from PySide2 import QtCore, QtGui, QtWidgets
import qimage2ndarray

from modules.game_func import Game

monitor = get_monitors()

m_width = monitor[0].width
m_height = monitor[0].height

spath = os.path.abspath('')[:-7] + '\\sounds'

is_Settings = False
octave3 = False
octave4 = False
octave5 = False
key_num_7 = False
key_num_14 = False
or_camera_1 = False
or_camera_2 = False


class Settings_Window(QtWidgets.QWidget):
    def __init__(self):
        super(Settings_Window, self).__init__()

        self.groupBox1 = QtWidgets.QGroupBox("Octave")
        self.radio11 = QtWidgets.QRadioButton("&C3")
        self.radio12 = QtWidgets.QRadioButton("&C4")
        self.radio13 = QtWidgets.QRadioButton("&C5")
        self.groupBox2 = QtWidgets.QGroupBox("Number of keys")
        self.radio21 = QtWidgets.QRadioButton("7")
        self.radio22 = QtWidgets.QRadioButton("14")
        self.groupBox3 = QtWidgets.QGroupBox("&Camera orientation")
        self.radio31 = QtWidgets.QRadioButton("-1")
        self.radio32 = QtWidgets.QRadioButton("1")
        self.confirm = QtWidgets.QPushButton('confirm')
        self.settings_ui()

    def settings_ui(self):

        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.setWindowTitle('Settings')

        grid = QtWidgets.QGridLayout()

        self.groupBox1.setFont(QtGui.QFont("Sanserif", 14))

        # radio11.setChecked(True)

        vbox1 = QtWidgets.QVBoxLayout()
        vbox1.addWidget(self.radio11)
        vbox1.addWidget(self.radio12)
        vbox1.addWidget(self.radio13)

        vbox1.addStretch(1)
        self.groupBox1.setLayout(vbox1)

        self.groupBox2.setFont(QtGui.QFont("Sanserif", 14))

        vbox2 = QtWidgets.QVBoxLayout()
        vbox2.addWidget(self.radio21)
        vbox2.addWidget(self.radio22)

        self.groupBox2.setEnabled(False)

        self.radio11.clicked.connect(self.radioButtonClicked)
        self.radio12.clicked.connect(self.radioButtonClicked)
        self.radio13.clicked.connect(self.radioButtonClicked)

        vbox2.addStretch(1)
        self.groupBox2.setLayout(vbox2)

        self.radio32.setChecked(True)
        vbox3 = QtWidgets.QHBoxLayout()
        vbox3.addWidget(self.radio31)
        vbox3.addWidget(self.radio32)

        vbox3.addStretch(1)
        self.groupBox3.setLayout(vbox3)

        grid.addWidget(self.groupBox1, 0, 0)
        grid.addWidget(self.groupBox2, 0, 1)
        grid.addWidget(self.groupBox3, 1, 0, 1, 2)

        grid.addWidget(self.confirm, 2, 0, 1, 2)

        self.setLayout(grid)

        self.resize(400, 300)

        self.confirm.clicked.connect(self.win_close)

    def radioButtonClicked(self):
        if self.radio13.isChecked():

            print(self.radio13.text())

            self.groupBox2.setEnabled(True)
            self.radio22.setEnabled(False)
            self.radio21.setChecked(True)
        else:
            self.groupBox2.setEnabled(True)
            self.radio22.setEnabled(True)

    # глупая защита

    def win_close(self):
        if (self.radio11.isChecked() or self.radio12.isChecked() or self.radio13.isChecked()) and (
                self.radio21.isChecked() or self.radio22.isChecked()):

            global octave3, octave4, octave5, key_num_7, key_num_14, is_Settings, or_camera_1, or_camera_2
            if self.radio11.isChecked():
                octave3 = True
            elif self.radio12.isChecked():
                octave4 = True
            else:
                octave5 = True
            if self.radio21.isChecked():
                key_num_7 = True
            else:
                key_num_14 = True
            if self.radio31.isChecked():
                or_camera_1 = True
            else:
                or_camera_2 = True

            is_Settings = True

            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Attention", "Please select all settings!")


class VideoPlayer(QtWidgets.QWidget):
    pause = False
    video = False

    def __init__(self, fps=30):

        self.w2 = Settings_Window()
        self.camera_capture = cv.VideoCapture(0, cv.CAP_DSHOW)
        self.video_capture = cv.VideoCapture()

        self.frame_timer = QtCore.QTimer()
        self.setup_camera(fps)

        self.fps = fps

        self.ret, self.img = self.camera_capture.read()
        self.height, self.width = self.img.shape[:2]
        self.pgame = Game(self.height, self.width, spath)

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

        QtWidgets.QWidget.__init__(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.move(m_width // 6, m_height // 8)
        self.setWindowTitle('Magic Piano')
        self.setFixedSize(self.sizeHint())

        # передали адрес функции
        self.quit_buttom.clicked.connect(self.close_win)

        self.setLayout(self.main_layout)

        QtWidgets.QToolTip.setFont(QtGui.QFont('Arial', 8))
        self.quit_buttom.setToolTip('<b>Click here to exit the app</b>')

        self.main_layout.addWidget(self.menu_bar(), 0, 0, 1, 2)

        # геолокация 1-2 клеточки 1-размер по высоте 2-по ширине
        self.main_layout.addWidget(self.frame_label, 1, 0, 1, 2)
        self.main_layout.addWidget(self.play_pause_buttom, 2, 0, 1, 1)
        self.main_layout.addWidget(self.camera_video_buttom, 2, 1, 1, 1)
        self.main_layout.addWidget(self.quit_buttom, 3, 0, 1, 2)

    def menu_bar(self):

        menu = QtWidgets.QMenuBar(self)
        file = menu.addMenu("File")
        # file.addAction("Select video")

        exit = QtWidgets.QAction('Quit', self)
        exit.setShortcut('Ctrl+E')
        # exit.setStatusTip('exit app')
        exit.triggered.connect(self.close_win)
        file.addAction(exit)

        edit = menu.addMenu("Edit")

        settings = QtWidgets.QAction('Settings', self)
        settings.setShortcut('Ctrl+R')
        settings.triggered.connect(self.show_window_2)

        edit.addAction(settings)

        return menu

    def show_window_2(self):
        self.w2.setWindowModality(QtCore.Qt.ApplicationModal)

        # в душе не знаю
        self.pause = True
        self.play_pause_buttom.setText('Play')
        self.frame_timer.stop()

        img = np.random.randint(255, size=(
            int(monitor[0].height / 1.5), int(monitor[0].width / 1.5), 3), dtype=np.uint8)

        image = qimage2ndarray.array2qimage(img)

        self.frame_label.setPixmap(QtGui.QPixmap.fromImage(image))

        self.w2.show()

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
            # пианино уменьшается
            ret, img = self.video_capture.read()

        if not self.ret:
            return False

        # if not self.video:

        global is_Settings, octave3, octave4, octave5, key_num_7, key_num_14, or_camera_1, or_camera_2
        if is_Settings:
            octave = None
            key_num = None
            turn = 1

            if octave3:
                octave3 = False
                octave = 3
            elif octave4:
                octave4 = False
                octave = 4
            else:
                octave5 = False
                octave = 5

            if key_num_7:
                key_num_7 = False
                key_num = 7
            else:
                key_num_14 = False
                key_num = 14
            if or_camera_1:
                or_camera_1 = False
                turn = -1
            else:
                or_camera_2 = False
                turn = 1

            self.pgame = Game(self.height, self.width, spath, turn, octave, key_num)

            is_Settings = False

        img = self.pgame.render(img)

        img = cv.resize(img, (int(m_width / 1.5), int(m_height / 1.5)),
                        interpolation=cv.INTER_AREA)

        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        image = qimage2ndarray.array2qimage(img)

        self.frame_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def close_win(self, event):

        self.frame_timer.stop()

        reply = QtWidgets.QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            cv.destroyAllWindows()
            self.camera_capture.release()
            self.close()
        else:
            self.frame_timer.start()
            return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setWindowIcon(QtGui.QIcon('../icon/icon.png'))
    player = VideoPlayer()
    player.show()

    sys.exit(app.exec_())
