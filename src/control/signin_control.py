import sys

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QThreadPool
from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QMainWindow, QLineEdit

from config.client_info import config, write_to_json
from config.front_end.icon_path import owl_gif, title_img, signin_icon
from config.sql_query.account_query import parent_id_check, parent_signin
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.base_lib.utils.aes_pass import AESCipher
from lib.pyqt_lib.message_box import message_info_box
from lib.pyqt_lib.query_handling import Worker
from src.control.famiowl_client_control import FamiOwlClientWindow
from src.control.signup_control import SignupWindow
from src.model.parent import Parent
from src.signin_window import Ui_Signin_Window

aes_cipher = AESCipher()
sql_utils = SqlUtils()


class SigninWindow(QMainWindow, Ui_Signin_Window):
    def __init__(self, parent=None):
        super(SigninWindow, self).__init__(parent)
        self.setupUi(self)
        self.signup_window = None
        self.start_x = None
        self.start_y = None
        self.threadpool = QThreadPool()

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
        else:
            if config['parent_id'] is not None:
                self.userid_line.setText(config['parent_id'])

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
            worker = Worker(self.__signin_query, id_input=self.__userid, pwd_input=self.__pwd)
            worker.signals.result.connect(self.__thread_result)
            worker.signals.finished.connect(self.__thread_complete)
            self.threadpool.start(worker)

            self.signin_button.setEnabled(False)
            self.userid_line.setEnabled(False)
            self.pwd_line.setEnabled(False)
            self.signup_button.setEnabled(False)
            self.forget_pwd_button.setEnabled(False)
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
        self.famiowl_client = FamiOwlClientWindow(parent_obj=self.__parent_obj)
        self.famiowl_client.show()
        self.close()

    def __signin_query(self, id_input, pwd_input):
        try:
            res = sql_utils.sql_exec(parent_id_check.format(id_input), 1)[0][0]
        except Exception as e:
            return 'Fetch parent info failed!'

        if res is None:
            return "Fetch parent info failed!"

        elif res == 0:
            return "User does not exist"

        try:
            res = sql_utils.sql_exec(parent_signin.format(id_input), 1)[0]
        except Exception as e:
            return 'Fetch parent info failed!'

        if not self.__verify_pwd(pwd_input, res[1]):
            return "Password Incorrect!"
        else:
            parent = Parent(self.__userid, res[0])
            self.__parent_obj = parent
            config['parent_id'] = id_input
            config['parent_name'] = res[0]
            config['parent_pwd'] = res[1]
            config['signin_state'] = True
            write_to_json()
            return True

    @staticmethod
    def __verify_pwd(user_input, pwd):
        try:
            if aes_cipher.decrypt_main(pwd) == user_input:
                return True
            else:
                return False
        except Exception as e:
            assert False, e

    def __thread_result(self, result):
        if result is True:
            self.__to_famiowl_client()
        else:
            message_info_box(self, str(result))

    def __thread_complete(self):
        self.signin_button.setEnabled(True)
        self.userid_line.setEnabled(True)
        self.pwd_line.setEnabled(True)
        self.signup_button.setEnabled(True)
        self.forget_pwd_button.setEnabled(True)
