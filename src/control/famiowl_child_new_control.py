from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow

from config.client_info import config
from config.sql_query.account_query import add_kid
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.pyqt_lib.message_box import message_info_box
from src.famiowl_child_new_window_Localicons import Ui_FamiOwlChildNew_localicons

# from src.famiowl_child_new_window import Ui_FamiOwlChildNew

sql_utils = SqlUtils()


class FamiOwlChildNew(QMainWindow, Ui_FamiOwlChildNew_localicons):
    def __init__(self, parent=None, kids=None):
        super(FamiOwlChildNew, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.pos_x = self.parent.pos().x()
        self.pos_y = self.parent.pos().y()
        self.start_x = None
        self.start_y = None
        self.iconindex = "0"
        self.__fill_in_buttons()

        self.kids = kids

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # self.__pop_up_position()

        self.__define_AddChild_button()

    def __define_AddChild_button(self):
        self.add_newchild_button.clicked.connect(lambda: self.__add_new_child())

    def __add_new_child(self):
        kidnum = len(self.kids)
        if (self.newchild_name.text() == ""):
            message_info_box(self, "Please enter your child`s name.")

        elif (self.iconindex == "0"):
            message_info_box(self, "Please select your profile icon.")
        elif (kidnum >= 4):
            message_info_box(self, "You`ve already got 4 child accounts.")
        else:
            sql_utils.sql_exec(
                add_kid.format(self.newchild_name.text(), str(config['parent_id']), self.iconindex, "120"), 0)
            message_info_box(self, "Child Added.")
            self.close()
            self.parent.close()

    def __fill_in_buttons(self):
        button_list = [self.pushButton_1, self.pushButton_2, self.pushButton_3, self.pushButton_4, self.pushButton_5,
                       self.pushButton_6
            , self.pushButton_7, self.pushButton_8, self.pushButton_9]
        for i in range(9):
            try:
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap("src/resource/profile_icons/" + str(i + 1) + ".png"),
                               QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
                button_list[i].setIcon(icon)
                button_list[i].setIconSize(QSize(100, 100))
            except IndexError as e:
                message_info_box(self, e)

        self.__define_buttons(button_list)

    def __define_buttons(self, button_list):
        self.pushButton_1.clicked.connect(lambda: self.__get_picked_icon_index("1", button_list))
        self.pushButton_2.clicked.connect(lambda: self.__get_picked_icon_index("2", button_list))
        self.pushButton_3.clicked.connect(lambda: self.__get_picked_icon_index("3", button_list))
        self.pushButton_4.clicked.connect(lambda: self.__get_picked_icon_index("4", button_list))
        self.pushButton_5.clicked.connect(lambda: self.__get_picked_icon_index("5", button_list))
        self.pushButton_6.clicked.connect(lambda: self.__get_picked_icon_index("6", button_list))
        self.pushButton_7.clicked.connect(lambda: self.__get_picked_icon_index("7", button_list))
        self.pushButton_8.clicked.connect(lambda: self.__get_picked_icon_index("8", button_list))
        self.pushButton_9.clicked.connect(lambda: self.__get_picked_icon_index("9", button_list))

    def __get_picked_icon_index(self, index, button_list):
        self.iconindex = index
        for i in range(9):
            if i != int(self.iconindex) - 1:
                button_list[i].setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                             "border :2px solid black")
            else:
                button_list[i].setStyleSheet("background-color: rgb(200, 200, 200);\n"
                                             "border :2px solid black")

    def __pop_up_position(self):
        if self.pos_x != 0 and self.pos_y != 0:
            self.move(self.pos_x, self.pos_y)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            super(FamiOwlChildNew, self).mousePressEvent(event)
            self.start_x = event.pos().x()
            self.start_y = event.pos().y()

    def mouseReleaseEvent(self, event):
        self.start_x = None
        self.start_y = None

    def mouseDoubleClickEvent(self, event):
        self.hide()
        # self.parent.show()

    def mouseMoveEvent(self, event):
        try:
            super(FamiOwlChildNew, self).mouseMoveEvent(event)
            dis_x = event.pos().x() - self.start_x
            dis_y = event.pos().y() - self.start_y
            self.move(self.x() + dis_x, self.y() + dis_y)
            self.parent.move(self.x() + dis_x, self.y() + dis_y)
        except:
            pass
