import sys

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QThreadPool
from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QMainWindow, QLineEdit

from config.client_info import config
from config.front_end.icon_path import owl_gif, title_img, signin_icon
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.base_lib.utils.aes_pass import AESCipher
from lib.business_lib.game_query import get_top_game_query
from lib.pyqt_lib.message_box import message_info_box
from lib.pyqt_lib.query_handling import Worker
from src.control.famiowl_client_control import FamiOwlClientWindow
from src.control.signup_control import SignupWindow
from src.model.fami_parent import FamiParent
from src.signin_window import Ui_Signin_Window

aes_cipher = AESCipher()
sql_utils = SqlUtils()


class SigninWindow(QMainWindow, Ui_Signin_Window):
    def __init__(self, parent=None, userid='', pwd='', parent_obj=None):
        super(SigninWindow, self).__init__(parent)
        self.setupUi(self)
        self.signup_window = None
        self.start_x = None
        self.start_y = None
        self.threadpool = QThreadPool()

        self.__userid = userid
        self.__pwd = pwd
        self.__parent_obj = parent_obj
        self.__top_games = []

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
        else:
            try:
                worker = Worker(self.__signin_query, id_input=self.__userid, pwd_input=self.__pwd)
                worker.signals.result.connect(self.__thread_result)
                worker.signals.finished.connect(self.__thread_complete)
                self.threadpool.start(worker)

                self.signin_button.setEnabled(False)
                self.userid_line.setEnabled(False)
                self.pwd_line.setEnabled(False)
                self.signup_button.setEnabled(False)
                # self.forget_pwd_button.setEnabled(False)
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
        self.famiowl_client = FamiOwlClientWindow(fami_parent=self.__parent_obj, top_games=self.__top_games)
        self.famiowl_client.show()
        self.close()

    def __signin_query(self, id_input, pwd_input):
        self.parent_obj = FamiParent()
        res = self.parent_obj.get_parent_info_query(id_input, pwd_input)
        id_res = []
        if isinstance(res, FamiParent):
            res = self.parent_obj.get_kids_info_query()
        if isinstance(res, FamiParent):
            self.parent_obj = res
            id_res = self.parent_obj.get_inventory_query()
        if not isinstance(res, str):
            top_games = get_top_game_query()
            self.__top_games = top_games
        else:
            return self.parent_obj
        for game in top_games:
            if int(game.return_game_id()) in id_res:
                game.run_game(self.parent_obj)

        return self.parent_obj, self.__top_games

    def __thread_result(self, result):
        if isinstance(result[0], FamiParent):
            # print(result.return_kids())
            self.__parent_obj = result[0]
            self.__top_games = result[1]
            self.__to_famiowl_client()
        else:
            message_info_box(self, 'Error Signin')

    def __thread_complete(self):
        self.signin_button.setEnabled(True)
        self.userid_line.setEnabled(True)
        self.pwd_line.setEnabled(True)
        self.signup_button.setEnabled(True)
        # self.forget_pwd_button.setEnabled(True)

    # Test Orientated
    def signin_query(self, id, pwd):
        self.__signin_query(id, pwd)
