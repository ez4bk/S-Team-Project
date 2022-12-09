from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow

from config.client_info import config, write_to_json
from config.front_end.front_end_var import to_add_new_child
from config.front_end.icon_path import add_child_icon
from src.control.famiowl_child_new_control import FamiOwlChildNew
from src.famiowl_child_selection_window import Ui_FamiOwlChildSelection


class FamiOwlChildSelectionWindow(QMainWindow, Ui_FamiOwlChildSelection):
    def __init__(self, parent=None, kids=None):
        super(FamiOwlChildSelectionWindow, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.pos_x = self.parent.pos().x()
        self.pos_x = self.parent.pos().x()
        self.pos_y = self.parent.pos().y()
        self.start_x = None
        self.start_y = None
        self.addnew_window = None

        self.kids = kids

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.__pop_up_position()
        self.__define_profile_buttons()

    def __pop_up_position(self):
        if self.pos_x != 0 and self.pos_y != 0:
            self.move(self.pos_x, self.pos_y)

    def __define_profile_buttons(self):
        profile_list = [self.child_profile_0, self.child_profile_1, self.child_profile_2, self.child_profile_3]
        profile_name_list = [self.child_name_0, self.child_name_1, self.child_name_2, self.child_name_3]

        for i in range(4):
            try:
                profile_name_list[i].setText(self.kids[i].return_kid_name())
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("src/resource/profile_icons/" + self.kids[i].return_profile() + ".png"),
                               QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
                profile_list[i].setIcon(icon)
                profile_list[i].setIconSize(QSize(100, 100))
                # profile_list[i].clicked.connect(lambda num=i: self.__save_child_select(profile_name_list[num].text()))
            except IndexError:
                profile_name_list[i].setText('Add New')
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(add_child_icon), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
                profile_list[i].setIcon(icon)
                profile_list[i].setIconSize(QSize(100, 100))
                profile_list[i].setObjectName(to_add_new_child)
                # profile_list[i].clicked.connect(lambda num=i: self.__add_new_child(num))

        self.__define_buttons()
    
    def __define_buttons(self):
        if self.child_profile_0.objectName() != to_add_new_child:
            self.child_profile_0.clicked.connect(lambda: self.__save_child_select(self.child_name_0.text(), 0))
        else:
            self.child_profile_0.clicked.connect(lambda: self.__add_new_child())

        if self.child_profile_1.objectName() != to_add_new_child:
            self.child_profile_1.clicked.connect(lambda: self.__save_child_select(self.child_name_1.text(), 1))
        else:
            self.child_profile_1.clicked.connect(lambda: self.__add_new_child())

        if self.child_profile_2.objectName() != to_add_new_child:
            self.child_profile_2.clicked.connect(lambda: self.__save_child_select(self.child_name_2.text(), 2))
        else:
            self.child_profile_2.clicked.connect(lambda: self.__add_new_child())

        if self.child_profile_3.objectName() != to_add_new_child:
            self.child_profile_3.clicked.connect(lambda: self.__save_child_select(self.child_name_3.text(), 3))
        else:
            self.child_profile_3.clicked.connect(lambda: self.__add_new_child())

    def __save_child_select(self, profile, index):
        config['current_child'] = profile
        config['profile_icon'] = self.kids[int(index)].return_profile()
        write_to_json()
        self.parent.setWindowTitle(self.parent.windowTitle() + " - " + profile)
        self.close()

    def __add_new_child(self):
        self.__goto_AddNewChild_window()

    def __goto_AddNewChild_window(self):
        self.addnew_window = FamiOwlChildNew(self, self.kids)
        if self.addnew_window.isVisible():
            self.addnew_window.hide()
        else:
            self.addnew_window.show()

    def mouseDoubleClickEvent(self, event):
        self.close()
        # if self.addnew_window is not None:
        #     if self.addnew_window.isVisible():
        #         self.addnew_window.close()
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
