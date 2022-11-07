from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow

from config.client_info import config
from config.front_end.icon_path import list_widget_icons, switch_child_icon
from src.control.famiowl_child_selection_control import FamiOwlChildSelectionWindow
from src.famiowl_client_window import Ui_FamiOwl


class FamiOwlClientWindow(QMainWindow, Ui_FamiOwl):
    def __init__(self, parent=None):
        super(FamiOwlClientWindow, self).__init__(parent)
        self.setupUi(self)
        self.child_selection_window = None
        self.start_x = None
        self.start_y = None

        self.parent_name_label.setText(config['parent_name'])

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.active_game_line.setAttribute(QtCore.Qt.WidgetAttribute.WA_MacShowFocusRect, 0)
        self.__create_game_widgets()
        self.__create_library_widget()
        self.__define_icons()
        self.__define_menu_listwidget()
        self.__define_switch_child_button()
        self.__sync_profile()

        self.menu_listwidget.setCurrentItem(self.menu_listwidget.itemAt(0, 0))
        self.stackedWidget.setCurrentWidget(self.game_page)

        if config['current_child'] is None:
            self.__to_child_selection_window()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            super(FamiOwlClientWindow, self).mousePressEvent(event)
            self.start_x = event.pos().x()
            self.start_y = event.pos().y()

    def mouseReleaseEvent(self, event):
        self.start_x = None
        self.start_y = None

    def mouseMoveEvent(self, event):
        try:
            super(FamiOwlClientWindow, self).mouseMoveEvent(event)
            dis_x = event.pos().x() - self.start_x
            dis_y = event.pos().y() - self.start_y
            self.move(self.x() + dis_x, self.y() + dis_y)
        except:
            pass

    def effect_shadow_style(self, widget):
        effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        effect_shadow.setOffset(12, 12)  # 偏移
        effect_shadow.setBlurRadius(128)  # 阴影半径
        effect_shadow.setColor(QColor(155, 230, 237, 150))  # 阴影颜色
        widget.setGraphicsEffect(effect_shadow)

    def __create_game_widgets(self):
        for i in range(5):
            game_card = QtWidgets.QWidget()
            game_card.setMinimumSize(QtCore.QSize(0, 121))
            game_card.setMaximumSize(QtCore.QSize(16777215, 121))
            game_card.setStyleSheet(".QWidget{\n"
                                    "    background-color: qlineargradient(x1:0, y0:0, x2:1, y2:0,stop:0 rgb(234, 249, 253), stop:1 rgb(155, 230, 237));\n"
                                    "    border-radius:20px;\n"
                                    "    color: rgb(255, 255, 255);\n"
                                    "}\n"
                                    "\n"
                                    "")
            game_card.setObjectName("game_card_%s" % i)
            game_card_layout = QtWidgets.QHBoxLayout(game_card)
            game_card_layout.setContentsMargins(24, 24, 24, 24)
            game_card_layout.setSpacing(24)
            game_card_layout.setObjectName("game_card_layout_%s" % i)
            game_profile_widget = QtWidgets.QWidget(game_card)
            game_profile_widget.setMaximumSize(QtCore.QSize(100, 16777215))
            game_profile_widget.setStyleSheet("image: url(:/svg/img/button_png/image.jpg);")
            game_profile_widget.setObjectName("game_profile_widget_%s" % i)
            game_card_layout.addWidget(game_profile_widget)
            game_info_layout = QtWidgets.QVBoxLayout()
            game_info_layout.setSpacing(2)
            game_info_layout.setObjectName("game_info_layout_%s" % i)
            game_name_label = QtWidgets.QLabel(game_card)
            font = QtGui.QFont()
            font.setPointSize(16)
            font.setBold(True)
            game_name_label.setFont(font)
            game_name_label.setStyleSheet("color: rgb(22, 54, 53)")
            game_name_label.setObjectName("game_name_label_%s" % i)
            game_name_label.setText("Game #%s" % i)
            game_info_layout.addWidget(game_name_label)
            game_info_label = QtWidgets.QLabel(game_card)
            font = QtGui.QFont()
            font.setBold(False)
            game_info_label.setFont(font)
            game_info_label.setStyleSheet("color: rgb(22, 54, 53)")
            game_info_label.setObjectName("game_info_label_%s" % i)
            game_info_label.setText("Game Info #%s" % i)
            game_info_layout.addWidget(game_info_label)
            time_limit_bar = QtWidgets.QProgressBar(game_card)
            time_limit_bar.setStyleSheet("QProgressBar::chunk {\n"
                                         "        border-top-left-radius:8px;\n"
                                         "border-bottom-left-radius:8px;\n"
                                         "    background-color: rgb(103, 216, 217)\n"
                                         "}\n"
                                         "QProgressBar{\n"
                                         "border-radius:8px;\n"
                                         "background-color: rgb(223, 223, 223);\n"
                                         "}\n"
                                         "")
            time_limit_bar.setProperty("value", 60)
            time_limit_bar.setTextVisible(False)
            time_limit_bar.setObjectName("time_limit_bar_%s" % i)
            game_info_layout.addWidget(time_limit_bar)
            game_card_layout.addLayout(game_info_layout)
            game_card_layout.setStretch(0, 1)

            self.verticalLayout_13.addWidget(game_card)

    def __define_icons(self):
        for i in range(4):
            item = self.menu_listwidget.item(i)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(list_widget_icons[i]),
                           QtGui.QIcon.Mode.Normal,
                           QtGui.QIcon.State.Off)
            item.setIcon(icon)
        self.switch_child_button.setStyleSheet("image: url(%s);" % switch_child_icon +
                                               "border-radius:32px;\n"
                                               "background-color: transparent;"
                                               )

    def __to_child_selection_window(self):
        self.child_selection_window = FamiOwlChildSelectionWindow(self)
        if self.child_selection_window.isVisible():
            self.child_selection_window.hide()
        else:
            # self.child_selection_window.
            self.child_selection_window.show()

    def __define_switch_child_button(self):
        self.switch_child_button.clicked.connect(lambda: self.__to_child_selection_window())

    def __define_menu_listwidget(self):
        self.menu_listwidget.itemClicked.connect(lambda: self.__menu_select())

    def __menu_select(self):
        item = self.menu_listwidget.currentItem()
        widget_to_go = item.text()
        if widget_to_go == 'Games':
            self.stackedWidget.setCurrentWidget(self.game_page)
        elif widget_to_go == 'Library':
            self.stackedWidget.setCurrentWidget(self.library_page)
        elif widget_to_go == 'Settings':
            self.stackedWidget.setCurrentWidget(self.setting_page)
        elif widget_to_go == 'Exit':
            # TODO: Separate sign-out and exit
            # config['signin_state'] = False
            # write_to_json()
            exit()

    def __create_library_widget(self):
        for i in range(10):
            game_card = QtWidgets.QWidget()
            game_card.setMinimumSize(QtCore.QSize(0, 121))
            game_card.setMaximumSize(QtCore.QSize(16777215, 121))
            game_card.setStyleSheet(".QWidget{\n"
                                    "    background-color: qlineargradient(x1:0, y0:0, x2:1, y2:0,stop:0 rgb(234, 249, 253), stop:1 rgb(155, 230, 237));\n"
                                    "    border-radius:20px;\n"
                                    "    color: rgb(255, 255, 255);\n"
                                    "}\n"
                                    "\n"
                                    "")
            game_card.setObjectName("game_card_%s" % i)
            game_card_layout = QtWidgets.QHBoxLayout(game_card)
            game_card_layout.setContentsMargins(24, 24, 24, 24)
            game_card_layout.setSpacing(24)
            game_card_layout.setObjectName("game_card_layout_%s" % i)
            game_profile_widget = QtWidgets.QWidget(game_card)
            game_profile_widget.setMaximumSize(QtCore.QSize(100, 16777215))
            game_profile_widget.setStyleSheet("image: url(:/svg/img/button_png/image.jpg);")
            game_profile_widget.setObjectName("game_profile_widget_%s" % i)
            game_card_layout.addWidget(game_profile_widget)
            game_info_layout = QtWidgets.QVBoxLayout()
            game_info_layout.setSpacing(2)
            game_info_layout.setObjectName("game_info_layout_%s" % i)
            game_name_label = QtWidgets.QLabel(game_card)
            font = QtGui.QFont()
            font.setPointSize(16)
            font.setBold(True)
            game_name_label.setFont(font)
            game_name_label.setStyleSheet("color: rgb(22, 54, 53)")
            game_name_label.setObjectName("game_name_label_%s" % i)
            game_name_label.setText("Game #%s" % i)
            game_info_layout.addWidget(game_name_label)
            game_info_label = QtWidgets.QLabel(game_card)
            font = QtGui.QFont()
            font.setBold(False)
            game_info_label.setFont(font)
            game_info_label.setStyleSheet("color: rgb(22, 54, 53)")
            game_info_label.setObjectName("game_info_label_%s" % i)
            game_info_label.setText("Game Info #%s" % i)
            game_info_layout.addWidget(game_info_label)
            time_limit_bar = QtWidgets.QProgressBar(game_card)
            time_limit_bar.setStyleSheet("QProgressBar::chunk {\n"
                                         "        border-top-left-radius:8px;\n"
                                         "border-bottom-left-radius:8px;\n"
                                         "    background-color: rgb(103, 216, 217)\n"
                                         "}\n"
                                         "QProgressBar{\n"
                                         "border-radius:8px;\n"
                                         "background-color: rgb(223, 223, 223);\n"
                                         "}\n"
                                         "")
            time_limit_bar.setProperty("value", 60)
            time_limit_bar.setTextVisible(False)
            time_limit_bar.setObjectName("time_limit_bar_%s" % i)
            game_info_layout.addWidget(time_limit_bar)
            game_card_layout.addLayout(game_info_layout)
            game_card_layout.setStretch(0, 1)

            self.verticalLayout_14.addWidget(game_card)

    def __sync_profile(self):
        self.windowTitleChanged.connect(lambda: self.__switch_child())

    def __switch_child(self):
        self.child_name_label.setText(config['current_child'])
        a = 'src/resource/like_icon.png'
        self.profile_image_widget.setStyleSheet("border-radius:32px;"
                                                "background-color: rgb(223, 223, 223);"
                                                "image: url(%s);" % a)
