import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QLineEdit

from config.sql_query.account_query import parent_signin
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.pyqt_lib.message_box import message_info_box
from src.signin_window import Ui_Signin_Window
from src.signup_control import SignupWindow

sql_utils = SqlUtils()


class SigninWindow(QMainWindow, Ui_Signin_Window):
    def __init__(self, parent=None):
        super(SigninWindow, self).__init__(parent)
        self.setupUi(self)
        self.signup_window = None

        self.__userid = ''
        self.__pwd = ''

        self.pwd_line.setEchoMode(QLineEdit.EchoMode.Password)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

        self.__define_exit_button()
        self.__define_signin_button()
        self.__define_signup_button()

    def __define_exit_button(self):
        self.exit_button.clicked.connect(lambda: sys.exit())

    def __define_signin_button(self):
        self.signin_button.clicked.connect(lambda: self.__signin())

    def __signin(self):
        try:
            self.__userid = str(self.userid_line.text())
            self.__pwd = str(self.pwd_line.text())
        except TypeError as e:
            message_info_box(self, e)

        signin_code = self.__signin_query()
        if signin_code == 0:
            message_info_box(self, "Sign in Successfully!")
            # time.sleep(5)
            # sys.exit()
        elif signin_code == 1:
            message_info_box(self, "Incorrect password!")
        elif signin_code == 2:
            message_info_box(self, "User does not exist. Sign up now!")
        elif signin_code == 3:
            message_info_box(self, "Empty User ID or Password!")

    def __signin_query(self):
        """
        Get all parents accounts information and find match. Return result code.
        :return: 0 Success, 1 pwd not match, 2 userid not found, 3 empty entry
        """
        if self.__userid == '' or self.__pwd == '':
            return 3

        parent_accounts = sql_utils.sql_exec(parent_signin, 1)
        for parent in parent_accounts:
            if parent[0] == self.__userid:
                if parent[2] == self.__pwd:
                    return 0
                else:
                    return 1
        return 2

    def __define_signup_button(self):
        self.signup_button.clicked.connect(lambda: self.__to_signup_window())

    def __to_signup_window(self):
        self.signup_window = SignupWindow(self)
        if self.signup_window.isVisible():
            self.signup_window.hide()
        else:
            self.hide()
            self.signup_window.show()
