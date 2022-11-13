import re

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QMainWindow, QLineEdit

from config.front_end.icon_path import child_img
from config.front_end.stylesheet import signup_button_ss, signup_button_disabled_ss
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.base_lib.utils.aes_pass import AESCipher
from lib.pyqt_lib.create_thread import create_thread
from lib.pyqt_lib.message_box import message_info_box
from lib.pyqt_lib.query_handling import QueryHandling
from src.signup_window import Ui_Signup_Window

sql_utils = SqlUtils()
aes_cipher = AESCipher()


class SignupWindow(QMainWindow, Ui_Signup_Window):
    def __init__(self, parent=None):
        super(SignupWindow, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.pos_x = self.parent.pos().x()
        self.pos_y = self.parent.pos().y()
        self.start_x = None
        self.start_y = None

        self.__userid = ''
        self.__username = ''
        self.__pwd = ''

        self.signup_pic.setPixmap(QtGui.QPixmap(child_img))

        self.signup_pwd_line.setEchoMode(QLineEdit.EchoMode.Password)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

        self.__define_back_button()
        self.__define_signup_button()
        self.__define_email_line()

    def mouseDoubleClickEvent(self, event):
        self.hide()
        self.parent.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            super(SignupWindow, self).mousePressEvent(event)
            self.start_x = event.pos().x()
            self.start_y = event.pos().y()

    def mouseReleaseEvent(self, event):
        self.start_x = None
        self.start_y = None

    def mouseMoveEvent(self, event):
        try:
            super(SignupWindow, self).mouseMoveEvent(event)
            dis_x = event.pos().x() - self.start_x
            dis_y = event.pos().y() - self.start_y
            self.move(self.x() + dis_x, self.y() + dis_y)
            self.parent.move(self.x() + dis_x, self.y() + dis_y)
        except:
            pass

    def __define_back_button(self):
        self.signup_back_button.clicked.connect(lambda: self.__back_to_signin())

    def __back_to_signin(self):
        if self.parent.isVisible():
            self.parent.hide()
        else:
            self.hide()
            self.parent.show()

    def __define_signup_button(self):
        self.signup_button.clicked.connect(lambda: self.__signup())

    def __signup(self):
        try:
            self.__userid = self.signup_email_line.text()
            self.__username = self.signup_username_line.text()
            self.__pwd = self.signup_pwd_line.text()
        except TypeError as e:
            message_info_box(self, e)

        if self.__userid == '' or self.__username == '' or self.__pwd == '':
            message_info_box(self, "Empty entry!")

        self.__pwd = aes_cipher.encrypt_main(self.__pwd)

        try:
            self.worker = QueryHandling(user_id=self.__userid, user_name=self.__username,
                                        pwd=self.__pwd, ui=self)
            self.thread = create_thread(self.worker, self.worker.handle_signup_query)
            self.thread.start()

            self.signup_button.setEnabled(False)
            self.signup_email_line.setEnabled(False)
            self.signup_pwd_line.setEnabled(False)
            self.signup_username_line.setEnabled(False)

            self.worker.error.connect(lambda: self.signup_button.setEnabled(True))
            self.worker.error.connect(lambda: self.signup_email_line.setEnabled(True))
            self.worker.error.connect(lambda: self.signup_pwd_line.setEnabled(True))
            self.worker.error.connect(lambda: self.signup_username_line.setEnabled(True))
            self.worker.error.connect(self.__error_msg_slot)
            self.thread.finished.connect(lambda: self.__signup_success())
        except AssertionError as e:
            message_info_box(self, e)

    def __define_email_line(self):
        self.signup_email_line.textChanged.connect(lambda: self.__validate_email())

    def __validate_email(self):
        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(email_regex, self.signup_email_line.text()):
            self.signup_button.setDisabled(True)
            self.signup_button.setStyleSheet(signup_button_disabled_ss)
            self.signup_button.setToolTip("Invalid E-mail")
        else:
            self.signup_button.setEnabled(True)
            self.signup_button.setStyleSheet(signup_button_ss)
            self.signup_button.setToolTip("")

    def __signup_success(self):
        self.hide()
        self.parent.show()

    @pyqtSlot(str)
    def __error_msg_slot(self, msg):
        message_info_box(self, msg)
