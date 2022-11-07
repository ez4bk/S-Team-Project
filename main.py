import sys

from PyQt6 import QtWidgets

from lib.base_lib.sql.sql_utils import SqlUtils
from src.control.signin_control import SigninWindow

# from src.control.famiowl_client_control import FamiOwlClientWindow

sql_utils = SqlUtils()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    signin_window = SigninWindow()
    signin_window.show()
    # w = FamiOwlClientWindow()
    # w.show()

    sys.exit(app.exec())
