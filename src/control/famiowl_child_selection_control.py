from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow

from config.client_info import config, write_to_json
from src.famiowl_child_selection_window import Ui_FamiOwlChildSelection


class FamiOwlChildSelectionWindow(QMainWindow, Ui_FamiOwlChildSelection):
    def __init__(self, parent=None):
        super(FamiOwlChildSelectionWindow, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.pos_x = self.parent.pos().x()
        self.pos_y = self.parent.pos().y()
        self.start_x = None
        self.start_y = None

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.__pop_up_position()
        self.__define_profile_buttons()

    def __pop_up_position(self):
        if self.pos_x != 0 and self.pos_y != 0:
            self.move(self.pos_x, self.pos_y)

    def __define_profile_buttons(self):
        self.child_profile_0.clicked.connect(lambda: self.__save_child_select(self.child_name_0.text()))
        self.child_profile_1.clicked.connect(lambda: self.__save_child_select(self.child_name_1.text()))
        self.child_profile_2.clicked.connect(lambda: self.__save_child_select(self.child_name_2.text()))
        self.child_profile_3.clicked.connect(lambda: self.__save_child_select(self.child_name_3.text()))

    def __save_child_select(self, profile):
        config['current_child'] = profile
        write_to_json()
        self.parent.setWindowTitle(self.parent.windowTitle() + " - " + profile)
        self.close()

    def mouseDoubleClickEvent(self, event):
        self.hide()
        self.parent.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            super(FamiOwlChildSelectionWindow, self).mousePressEvent(event)
            self.start_x = event.pos().x()
            self.start_y = event.pos().y()

    def mouseReleaseEvent(self, event):
        self.start_x = None
        self.start_y = None

    def mouseMoveEvent(self, event):
        try:
            super(FamiOwlChildSelectionWindow, self).mouseMoveEvent(event)
            dis_x = event.pos().x() - self.start_x
            dis_y = event.pos().y() - self.start_y
            self.move(self.x() + dis_x, self.y() + dis_y)
            self.parent.move(self.x() + dis_x, self.y() + dis_y)
        except:
            pass
