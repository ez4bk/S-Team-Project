import sys

from PyQt6 import QtWidgets, QtCore

from src.signin_window import Ui_Signin_Window

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
    ui = Ui_Signin_Window()
    ui.setupUi(window)
    window.resize(800, 450)
    window.show()
    sys.exit(app.exec())
