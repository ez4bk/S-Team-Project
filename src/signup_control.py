from PyQt6.QtWidgets import QMainWindow, QLineEdit

from config.sql_query.account_query import parent_signup, parent_signin
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.pyqt_lib.message_box import message_info_box
from src.signup_window import Ui_Signup_Window

sql_utils = SqlUtils()


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
