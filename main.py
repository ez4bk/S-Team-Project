import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLineEdit

from config.sql_query.account_query import *
from lib.base_lib.sql.sql_utils import SqlUtils
from src.signin_window import Ui_Signin_Window
from src.signup_window import Ui_Signup_Window

sql_utils = SqlUtils()


def message_info_box(parent, msg_str):
    """
    Pull up a message box.

    :param parent: parent window the msg box belongs to
    :param msg_str: message text
    :return: Null
    """
    QMessageBox.information(parent, 'FamiOwl Information', msg_str)


class SigninWindow(QMainWindow, Ui_Signin_Window):
    def __init__(self, parent=None):
        super(SigninWindow, self).__init__(parent)
        self.setupUi(self)
        self.signup_window = None

        self.__userid = ''
        self.__pwd = ''

        self.pwd_line.setEchoMode(QLineEdit.EchoMode.Password)

        self.__define_exit_button()
        self.__define_signin_button()
        self.__define_signup_button()

    def __define_exit_button(self):
        self.exit_button.clicked.connect(lambda: sys.exit(app.exec()))

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


class SignupWindow(QMainWindow, Ui_Signup_Window):
    def __init__(self, parent=None):
        super(SignupWindow, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)

        self.__userid = ''
        self.__username = ''
        self.__pwd = ''

        self.signup_pwd_line.setEchoMode(QLineEdit.EchoMode.Password)
        self.__define_back_button()
        self.__define_signup_button()

    def __define_back_button(self):
        self.signup_back_button.clicked.connect(lambda: self.__back_to_signin())

    def __back_to_signin(self):
        if signin_window.isVisible():
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
        result_code = self.__signup_query()
        if result_code == 1:
            message_info_box(self, "E-mail already registered!")
        elif result_code == 2:
            message_info_box(self, "Empty entry!")
        elif result_code == 0:
            message_info_box(self, "You have signed up successfully!")

    def __signup_query(self):
        """
        Insert a new account to parent table.
        :return: result code, 0 success, 1 duplicate, 2 empty entry
        """
        if self.__userid == '' or self.__username == '' or self.__pwd == '':
            return 2

        parent_accounts = sql_utils.sql_exec(parent_signin, 1)
        for parent in parent_accounts:
            if parent[0] == self.__userid:
                return 1
        signup_query = parent_signup.format(self.__userid, self.__username, self.__pwd)
        sql_utils.sql_exec(signup_query, 0)
        return 0


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    signin_window = SigninWindow()
    signin_window.show()

    sys.exit(app.exec())
