import sys

from PyQt6.QtWidgets import QMainWindow, QMessageBox

from config.sql_query.account_query import *
from lib.base_lib.sql.sql_utils import SqlUtils
from src.signin_window import *
from src.signup_window import *


class SigninWindow(QMainWindow, Ui_Signin_Window):
    def __init__(self, parent=None):
        super(SigninWindow, self).__init__(parent)
        self.setupUi(self)

    def message_info_box(self, msg_str):
        """
        Pull up a message box.
        :param msg_str: message text
        :return: Null
        """
        button = QMessageBox.information(self, 'FamiOwl Information', msg_str)
        # msg_box.setStyleSheet('blackground-color: black;'
        #                       'color: white;')
        # msg_box.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        # msg_box.exec()


class SignupWindow(QMainWindow, Ui_Signup_Window):
    def __int__(self, parent=None):
        super(SignupWindow, self).__init__(parent)
        self.setupUi(self)


def define_exit_button(exit_button):
    exit_button.clicked.connect(lambda: sys.exit(app.exec()))


def define_signin_button(signin_button, userid_line, pwd_line):
    try:
        userid = str(userid_line.text())
        pwd = str(pwd_line.text())
    except TypeError as e:
        pass
    signin_button.clicked.connect(lambda: signin(userid, pwd))


def signin(userid, pwd):
    signin_code = signin_query(userid, pwd)
    if signin_code == 0:
        pass
    elif signin_code == 1:
        signin_window.message_info_box("Incorrect password!")
    elif signin_code == 2:
        signin_window.message_info_box("User does not exist. Sign up now!")


def signin_query(userid, pwd):
    """
    Get all parents accounts information and find match. Return result code.
    :param userid: parent email to be found
    :param pwd: parent password to match
    :return: 0 Success, 1 pwd not match, 2 userid not found
    """
    sql_utils = SqlUtils()
    parent_accounts = sql_utils.sql_exec(parent_signin, 1)
    for parent in parent_accounts:
        if parent[0] == userid:
            if parent[2] == pwd:
                return 0
            else:
                return 1
    return 2


# def define_signup_button(signup_button):
#     signup_button.clicked.connect(lambda: to_signup_window())


# def to_signup_window():
#     signup_window = SignupWindow()
#     signup_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    signin_window = SigninWindow()
    # signin_window.show()

    signup_window = SignupWindow()
    signup_window.show()

    define_exit_button(signin_window.exit_button)
    define_signin_button(signin_window.signin_button, signin_window.userid_line, signin_window.pwd_line)
    # define_signup_button(signin_window.signup_button)
    sys.exit(app.exec())
