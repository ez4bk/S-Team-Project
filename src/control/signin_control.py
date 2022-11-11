import sys

from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QMainWindow, QLineEdit

from config.client_info import config, write_to_json
from config.front_end.icon_path import owl_gif, title_img, signin_icon
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.base_lib.utils.aes_pass import AESCipher
from lib.pyqt_lib.create_thread import create_thread
from lib.pyqt_lib.message_box import message_info_box
from lib.pyqt_lib.query_handling import QueryHandling
from src.control.famiowl_client_control import FamiOwlClientWindow
from src.control.signup_control import SignupWindow
from src.signin_window import Ui_Signin_Window

sql_utils = SqlUtils()
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
            config['parent_id'] = self.__userid
            write_to_json()
        except TypeError as e:
            message_info_box(self, e)

        if self.__userid == '' or self.__pwd == '':
            message_info_box(self, "Empty User ID or Password!")

        # self.thread = QThread()
        self.worker = QueryHandling(ui=self)
        # self.query.moveToThread(self.thread)
        # self.thread.started.connect(self.query.handle_signin_query)
        # self.query.finished.connect(self.thread.quit)
        # self.query.finished.connect(self.query.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        self.thread = create_thread(self.worker, self.worker.handle_signin_query)
        self.thread.start()

        self.signin_button.setEnabled(False)
        self.userid_line.setEnabled(False)
        self.pwd_line.setEnabled(False)
        self.thread.finished.connect(lambda: self.signin_button.setEnabled(True))
        self.thread.finished.connect(lambda: self.userid_line.setEnabled(True))
        self.thread.finished.connect(lambda: self.pwd_line.setEnabled(True))
        self.thread.finished.connect(lambda: self.__verify_pwd())

    def __verify_pwd(self):
        if config['parent_id'] is None:
            message_info_box(self, "User does not exist!")
        else:
            res = config['parent_pwd']
            try:
                if aes_cipher.decrypt_main(res) == self.__pwd:
                    config['signin_state'] = True
                    write_to_json()
                    self.__to_famiowl_client()

                else:
                    message_info_box(self, "Password incorrect!")
            except Exception as e:
                message_info_box(self, e.__str__())

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
