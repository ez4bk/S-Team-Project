import sys

from PyQt6 import QtWidgets

from lib.base_lib.sql.sql_utils import SqlUtils
from src.control.signin_control import SigninWindow

sql_utils = SqlUtils()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    signin_window = SigninWindow()
    signin_window.show()

    sys.exit(app.exec())
