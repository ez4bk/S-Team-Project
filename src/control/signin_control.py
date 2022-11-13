import sys

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QMainWindow, QLineEdit

from config.client_info import config
from config.front_end.icon_path import owl_gif, title_img, signin_icon
from lib.base_lib.utils.aes_pass import AESCipher
from lib.pyqt_lib.create_thread import create_thread
from lib.pyqt_lib.message_box import message_info_box
from lib.pyqt_lib.query_handling import QueryHandling
from src.control.famiowl_client_control import FamiOwlClientWindow
from src.control.signup_control import SignupWindow
from src.signin_window import Ui_Signin_Window

aes_cipher = AESCipher()


class SigninWindow(QMainWindow, Ui_Signin_Window):
    def __init__(self, parent=None):
        super(SigninWindow, self).__init__(parent)
        self.setupUi(self)
        self.signup_window = None
        self.start_x = None
        self.start_y = None

        self.__userid = ''
        self.__pwd = ''
        self.__parent_obj = None

        self.famiowl_title_label.setPixmap(QtGui.QPixmap(title_img))
        self.owl_gif_movie = QMovie(owl_gif)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(signin_icon), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.signin_button.setIcon(icon)
        self.signin_button.setIconSize(QtCore.QSize(60, 60))
        if config['signin_state']:
            self.userid_line.setText(config['parent_id'])
            self.pwd_line.setText(aes_cipher.decrypt_main(config['parent_pwd']))
            self.__signin()

        self.pwd_line.setEchoMode(QLineEdit.EchoMode.Password)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

        self.__define_exit_button()
        self.__define_signin_button()
        self.__define_signup_button()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            super(SigninWindow, self).mousePressEvent(event)
            self.start_x = event.pos().x()
            self.start_y = event.pos().y()

    def mouseReleaseEvent(self, event):
        self.start_x = None
        self.start_y = None

    def mouseMoveEvent(self, event):
        try:
            super(SigninWindow, self).mouseMoveEvent(event)
            dis_x = event.pos().x() - self.start_x
            dis_y = event.pos().y() - self.start_y
            self.move(self.x() + dis_x, self.y() + dis_y)
        except:
            pass

    def __define_exit_button(self):
        self.exit_button.clicked.connect(lambda: sys.exit())

    def __define_signin_button(self):
        self.pwd_line.returnPressed.connect(lambda: self.__signin())
        self.signin_button.clicked.connect(lambda: self.__signin())

    def __signin(self):
        try:
            self.__userid = str(self.userid_line.text())
            self.__pwd = str(self.pwd_line.text())
            if self.__userid != config['parent_id']:
                config['default_child'] = None
                config['current_child'] = None
        except TypeError as e:
            message_info_box(self, e)

        if self.__userid == '' or self.__pwd == '':
            message_info_box(self, "Empty User ID or Password!")

        try:
            self.worker = QueryHandling(ui=self, id_input=self.__userid, pwd_input=self.__pwd)
            self.thread = create_thread(self.worker, self.worker.handle_signin_query)
            self.thread.start()

            self.signin_button.setEnabled(False)
            self.userid_line.setEnabled(False)
            self.pwd_line.setEnabled(False)
            self.signup_button.setEnabled(False)
            self.forget_pwd_button.setEnabled(False)
            self.worker.finished.connect(lambda: self.__to_famiowl_client())
            self.worker.error.connect(lambda: self.signin_button.setEnabled(True))
            self.worker.error.connect(lambda: self.userid_line.setEnabled(True))
            self.worker.error.connect(lambda: self.pwd_line.setEnabled(True))
            self.worker.error.connect(lambda: self.signup_button.setEnabled(True))
            self.worker.error.connect(lambda: self.forget_pwd_button.setEnabled(True))
            self.worker.error.connect(self.__error_msg_slot)
        except Exception as e:
            message_info_box(self, e)

    def __define_signup_button(self):
        self.signup_button.clicked.connect(lambda: self.__to_signup_window())

    def __to_signup_window(self):
        self.signup_window = SignupWindow(self)
        if self.signup_window.isVisible():
            self.signup_window.hide()
        else:
            self.hide()
            self.signup_window.show()

    def __to_famiowl_client(self):
        self.famiowl_client = FamiOwlClientWindow()
        self.famiowl_client.show()
        self.close()

    @pyqtSlot(str)
    def __error_msg_slot(self, msg):
        message_info_box(self, msg)
