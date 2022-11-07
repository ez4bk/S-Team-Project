from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow

from config.client_info import config, write_to_json
from config.sql_query.account_query import kids_select
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.pyqt_lib.message_box import message_info_box

from src.famiowl_child_selection_window import Ui_FamiOwlChildSelection

sql_utils = SqlUtils()

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

        kids = self.__kids_query()
        # list_id = [sub[0] for sub in kids] # list of kids' id of this parent
        list_name = [sub[1] for sub in kids] # list of kids' name of this parent
        list_icon = [sub[3] for sub in kids] # list of kids' icon of this parent

        self.__pop_up_position()
        self.__define_profile_buttons(list_name,list_icon)

    def __kids_query(self):
        try:
            # store this parent's kids' info into a list
            info = sql_utils.sql_exec(kids_select.format(config['parent_id']))
            return info
        except Exception as e:
            message_info_box(self, e)
        return None

    def __pop_up_position(self):
        if self.pos_x != 0 and self.pos_y != 0:
            self.move(self.pos_x, self.pos_y)

    def __define_profile_buttons(self,list_name,list_icon):
        if (len(list_name) >= 1):
            self.child_profile_0.clicked.connect(lambda: self.__save_child_select(list_name[0],list_icon[0]))
            self.child_name_0.setText(list_name[0])
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("src/resource/profile_icons/" + list_icon[0] + ".png"),
                           QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
            self.child_profile_0.setIcon(icon)
            self.child_profile_0.setIconSize(QSize(100, 100))
        if (len(list_name) >= 2):
            self.child_profile_1.clicked.connect(lambda: self.__save_child_select(list_name[1],list_icon[1]))
            self.child_name_1.setText(list_name[1])
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("src/resource/profile_icons/" + list_icon[1] + ".png"),
                           QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
            self.child_profile_1.setIcon(icon)
            self.child_profile_1.setIconSize(QSize(100, 100))
        if (len(list_name) >= 3):
            self.child_profile_2.clicked.connect(lambda: self.__save_child_select(list_name[2],list_icon[2]))
            self.child_name_2.setText(list_name[2])
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("src/resource/profile_icons/" + list_icon[2] + ".png"),
                           QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
            self.child_profile_2.setIcon(icon)
            self.child_profile_2.setIconSize(QSize(100, 100))
        if (len(list_name) >= 4):
            self.child_profile_3.clicked.connect(lambda: self.__save_child_select(list_name[3],list_icon[3]))
            self.child_name_3.setText(list_name[3])
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("src/resource/profile_icons/" + list_icon[3] + ".png"),
                           QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
            self.child_profile_3.setIcon(icon)
            self.child_profile_3.setIconSize(QSize(100, 100))


    def __save_child_select(self, profile,index):
        config['current_child'] = profile
        config['profile_icon'] = index
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
