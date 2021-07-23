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

mpath = os.path.abspath('')[:-7] + 'music\\'

is_Settings = False
octave3 = False
octave4 = False
octave5 = False
key_num_7 = False
key_num_14 = False
or_camera_1 = False
or_camera_2 = False

db_mode = True
time = 0
miss = 0
time_stop = 0
timeline = []
step = 0

class Settings_Window(QtWidgets.QWidget):
    def __init__(self):
        super(Settings_Window, self).__init__()

        self.debug_mode = QtWidgets.QCheckBox('Debug mode')
        self.debug_mode.toggle()

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

        grid.addWidget(self.debug_mode, 0, 0)
        grid.addWidget(self.groupBox1, 1, 0)
        grid.addWidget(self.groupBox2, 1, 1)
        grid.addWidget(self.groupBox3, 2, 0, 1, 2)

        grid.addWidget(self.confirm, 3, 0, 1, 2)

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

            global octave3, octave4, octave5, key_num_7, key_num_14, is_Settings, or_camera_1, or_camera_2, db_mode
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

            if self.debug_mode.isChecked():
                db_mode = True
            else:
                db_mode = False

            is_Settings = True

            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Attention", "Please select all settings!")


class VideoPlayer(QtWidgets.QWidget):
    pause = False
    video = False
    mus = False

    def __init__(self, fps=30):

        self.w2 = Settings_Window()
        self.camera_capture = cv.VideoCapture(0, cv.CAP_DSHOW)
        self.video_capture = cv.VideoCapture()

        self.out = cv.VideoWriter('test.avi', cv.VideoWriter_fourcc(*'MJPG'), 20,
                                  (int(m_width / 1.5), int(m_height / 1.5)))

        self.test = cv.VideoCapture(os.path.abspath('')[:-7] + 'music\\a-tisket-a-tasket-c4-c5-11.mp4')

        self.frame_timer = QtCore.QTimer()
        self.music_timer = QtCore.QTimer()
        self.setup_camera(fps)

        self.fps = fps

        self.ret, self.img = self.camera_capture.read()
        self.height, self.width = self.img.shape[:2]
        self.pgame = Game(self.height, self.width, spath)

        #self.mgame = Game(self.height, self.width, spath, 1, 4, 14, os.path.abspath('')[:-7] + 'music\\a-tisket-a-tasket-c4-c5-11.txt')
        self.octave = None
        self.key_num = None

        # в Qt label работает для вывода изображения
        self.frame_label = QtWidgets.QLabel()
        #self.music_label = QtWidgets.QLabel()
        self.quit_buttom = QtWidgets.QPushButton('Quit')
        self.play_pause_buttom = QtWidgets.QPushButton('Pause')
        self.camera_video_buttom = QtWidgets.QPushButton('Switch to video')
        self.switch_to_music = QtWidgets.QPushButton('Switch to music')

        self.main_layout = QtWidgets.QGridLayout()

        self.setup_ui()

        # передали адрес функции
        self.quit_buttom.clicked.connect(self.close_win)
        self.play_pause_buttom.clicked.connect(self.play_pause)
        self.camera_video_buttom.clicked.connect(self.camera_video)
        self.switch_to_music.clicked.connect(self.select_video_music)

    def setup_ui(self):

        QtWidgets.QWidget.__init__(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.move(m_width // 6, m_height // 8)
        self.setWindowTitle('Magic Piano')
        self.setFixedSize(self.sizeHint())

        self.setLayout(self.main_layout)

        QtWidgets.QToolTip.setFont(QtGui.QFont('Arial', 8))
        self.quit_buttom.setToolTip('<b>Click here to exit the app</b>')

        self.main_layout.addWidget(self.menu_bar(), 0, 0, 1, 2)

        # геолокация 1-2 клеточки 1-размер по высоте 2-по ширине
        #
        #self.main_layout.addWidget(self.music_label, 1, 0, 1, 2)
        self.switch_to_music.setStyleSheet('border-style: solid; border-width: 3px; border-color: black;')
        self.play_pause_buttom.setStyleSheet('border-style: solid; border-width: 3px; border-color: black;')
        self.camera_video_buttom.setStyleSheet('border-style: solid; border-width: 3px; border-color: black;')
        self.quit_buttom.setStyleSheet('border-style: solid; border-width: 3px; border-color: red;')
        self.switch_to_music.setFont(QtGui.QFont('Arial', 20, QtGui.QFont.Bold))
        self.play_pause_buttom.setFont(QtGui.QFont('Arial', 20, QtGui.QFont.Bold))
        self.camera_video_buttom.setFont(QtGui.QFont('Arial', 20, QtGui.QFont.Bold))
        self.quit_buttom.setFont(QtGui.QFont('Arial', 20, QtGui.QFont.Bold))
        self.main_layout.addWidget(self.switch_to_music, 2, 0, 1, 2)
        self.main_layout.addWidget(self.frame_label, 3, 0, 1, 2)
        self.main_layout.addWidget(self.play_pause_buttom, 4, 0, 1, 1)
        self.main_layout.addWidget(self.camera_video_buttom, 4, 1, 1, 1)
        self.main_layout.addWidget(self.quit_buttom, 5, 0, 1, 2)

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

        music = menu.addMenu("Music")

        atat = QtWidgets.QAction('A Tisket, A Tasket', self)
        atat.setShortcut('Ctrl+1')
        atat.triggered.connect(self.atat)

        fj = QtWidgets.QAction('Frere Jacques', self)
        fj.setShortcut('Ctrl+2')
        fj.triggered.connect(self.fj)

        lb = QtWidgets.QAction('London Bridge', self)
        lb.setShortcut('Ctrl+3')
        lb.triggered.connect(self.lb)

        music.addAction(atat)
        music.addAction(fj)
        music.addAction(lb)

        return menu

    def atat(self):
        global miss, time, time_stop, timeline, step
        miss, time, time_stop, step = 0, 0, 24.1, 0
        timeline = []
        with open(mpath + 'a-tisket-a-tasket-timeline.txt', 'r') as p:
            times = p.read().split('\n')
        for t in times:
            codes = t.split(' ')
            timeline.append([codes[0], codes[1]])
        self.music_timer.stop()
        self.music_timer.start(int(1000//self.fps))
        self.mgame = Game(self.height, self.width, spath, 1, 4, 11, mpath + 'a-tisket-a-tasket-c4-c5-11.txt')


    def fj(self):
        global miss, time, time_stop, timeline, step
        miss, time, time_stop, step = 0, 0, 23.5, 0
        timeline = []
        with open(mpath + 'frere-jacques-timeline.txt', 'r') as p:
            times = p.read().split('\n')
        for t in times:
            codes = t.split(' ')
            timeline.append([codes[0], codes[1]])
        self.music_timer.stop()
        self.music_timer.start(int(1000//self.fps))
        self.mgame = Game(self.height, self.width, spath, 1, 3, 13, mpath + 'frere-jacques-c3-c4-13.txt')

    def lb(self):
        global miss, time, time_stop, timeline, step
        miss, time, time_stop, step = 0, 0, 14.2, 0
        timeline = []
        with open(mpath + 'london-bridge-timeline.txt', 'r') as p:
            times = p.read().split('\n')
        for t in times:
            codes = t.split(' ')
            timeline.append([codes[0], codes[1]])
        self.music_timer.stop()
        self.music_timer.start(int(1000//self.fps))
        self.mgame = Game(self.height, self.width, spath, 1, 3, 11, mpath + 'london-bridge-c3-c4-11.txt')

    def show_window_2(self):
        self.w2.setWindowModality(QtCore.Qt.ApplicationModal)
        self.w2.show()

    def play_pause(self):
        if not self.pause:
            self.frame_timer.stop()
            #
            self.music_timer.stop()
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
        #
        self.music_timer.timeout.connect(self.music_stream)
        # timer (msec)
        #
        #self.music_timer.start(int(1000 // fps))
        self.frame_timer.start(int(1000 // fps))

    def select_video_music(self):
        if not self.mus:
            self.frame_timer.stop()
            #self.music_timer.start()
            self.switch_to_music.setText('Switch to FreeGame')
        else:
            self.frame_timer.start()
            self.music_timer.stop()
            self.switch_to_music.setText('Switch to music')
        self.mus = not self.mus

    def music_stream(self):
        global time
        #print(self.music_timer.interval())
        if (time*self.music_timer.interval())/1000 > time_stop:
            self.music_timer.stop()
        time += 1
       # ret, test = self.test.read()
        ret, img = self.camera_capture.read()
        if img is None:
            return
        else:
            global miss, step
            img, m = self.mgame.render(img, time * self.music_timer.interval() / 1000, db_mode)
            miss += m
            if time * self.music_timer.interval() / 1000 > float(timeline[step][1]):
                step += 1
            cv.putText(img, 'Number of misses : {}'.format(str(miss)), (50, 300),
                       cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            cv.putText(img, timeline[step][0] + ' ' + str(float('{:.1f}'.format(float(timeline[step][1])
                                                                                - time * self.music_timer.interval() / 1000))), (50, 450),
                       cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

            img = cv.resize(img, (int(m_width / 1.5), int(m_height / 1.5)),
                            interpolation=cv.INTER_AREA)

            # cv.imshow('tets',test)

            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            image = qimage2ndarray.array2qimage(img)

            self.frame_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def display_video_stream(self):
        if not self.video:
            ret, img = self.camera_capture.read()
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
        else:
            ret, img = self.video_capture.read()
            if img is None:
                return
            else:
                img = cv.resize(img, (640, 480),
                                interpolation=cv.INTER_AREA)

        if not self.ret:
            return False

        # if not self.video:
        img, miss = self.pgame.render(img, 0, db_mode)

        img = cv.resize(img, (int(m_width / 1.5), int(m_height / 1.5)),
                        interpolation=cv.INTER_AREA)

        self.out.write(img)
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
            self.video_capture.release()
            self.test.release()
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
