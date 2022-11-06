# Form implementation generated from reading ui file 'famiowl_client.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FamiOwl(object):
    def setupUi(self, FamiOwl):
        FamiOwl.setObjectName("FamiOwl")
        FamiOwl.resize(900, 600)
        FamiOwl.setStyleSheet("QScrollBar:horizontal{\n"
"    height:8px;\n"
"    background:rgba(0,0,0,0%);\n"
"border-radius:4px;\n"
"\n"
"}\n"
"QScrollBar::handle:horizontal{\n"
"    background:rgba(125,125,125,50%);\n"
"border-radius:4px;\n"
"}\n"
"QScrollBar::handle:horizontal:hover{\n"
"    background:rgba(125,125,125,100%);\n"
"    min-width:0;\n"
"}\n"
"QScrollBar::add-line:horizontal{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::sub-line:horizontal{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::add-line:horizontal:hover{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::sub-line:horizontal:hover{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::add-page:horizontal,QScrollBar::sub-page:horizontal\n"
"{\n"
"    background:rgba(0,0,0,10%);\n"
"    border-radius:4px;\n"
"}\n"
"\n"
"QScrollBar:vertical{\n"
"    width:8px;\n"
"    background:rgba(0,0,0,0%);\n"
"\n"
"}\n"
"QScrollBar::handle:vertical{\n"
"    width:0px;\n"
"    background:rgba(125,125,125,50%);\n"
"    border-radius:4px;\n"
"}\n"
"QScrollBar::handle:vertical:hover{\n"
"    width:0px;\n"
"    background:rgba(125,125,125,100%);\n"
"    border-radius:4px;\n"
"    min-width:20;\n"
"}\n"
"QScrollBar::add-line:vertical{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::sub-line:vertical{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::add-line:vertical:hover{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::sub-line:vertical:hover{\n"
"    height:0px;width:0px;\n"
"\n"
"}\n"
"QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical\n"
"{\n"
"    background:rgba(0,0,0,10%);\n"
"    border-radius:4px;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(FamiOwl)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.central_frame = QtWidgets.QFrame(self.centralwidget)
        self.central_frame.setStyleSheet("QFrame#central_frame{\n"
"    background-color: rgb(235, 235, 235);\n"
"    border-radius:20px;\n"
"}")
        self.central_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.central_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.central_frame.setObjectName("central_frame")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.central_frame)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(12)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.profile_frame = QtWidgets.QFrame(self.central_frame)
        self.profile_frame.setStyleSheet("QFrame#profile_frame{\n"
"    background-color: rgba(255, 255, 255, 0.8);\n"
"    border-radius:20px;\n"
"}")
        self.profile_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.profile_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.profile_frame.setObjectName("profile_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.profile_frame)
        self.verticalLayout_2.setContentsMargins(-1, -1, -1, 36)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.profile_image_frame = QtWidgets.QFrame(self.profile_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profile_image_frame.sizePolicy().hasHeightForWidth())
        self.profile_image_frame.setSizePolicy(sizePolicy)
        self.profile_image_frame.setStyleSheet("border:none")
        self.profile_image_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.profile_image_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.profile_image_frame.setObjectName("profile_image_frame")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.profile_image_frame)
        self.horizontalLayout_6.setContentsMargins(-1, 24, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.profile_image_widget = QtWidgets.QWidget(self.profile_image_frame)
        self.profile_image_widget.setMinimumSize(QtCore.QSize(65, 65))
        self.profile_image_widget.setMaximumSize(QtCore.QSize(65, 65))
        self.profile_image_widget.setStyleSheet("border-radius:32px;\n"
"background-color: rgb(223, 223, 223);")
        self.profile_image_widget.setObjectName("profile_image_widget")
        self.horizontalLayout_6.addWidget(self.profile_image_widget)
        self.verticalLayout_2.addWidget(self.profile_image_frame)
        self.parent_name_label = QtWidgets.QLabel(self.profile_frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.parent_name_label.setFont(font)
        self.parent_name_label.setStyleSheet("color: rgb(22, 54, 53)")
        self.parent_name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.parent_name_label.setObjectName("parent_name_label")
        self.verticalLayout_2.addWidget(self.parent_name_label)
        self.child_name_label = QtWidgets.QLabel(self.profile_frame)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.child_name_label.setFont(font)
        self.child_name_label.setStyleSheet("color: rgb(102, 128, 127);")
        self.child_name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.child_name_label.setObjectName("child_name_label")
        self.verticalLayout_2.addWidget(self.child_name_label)
        self.menu_listwidget = QtWidgets.QListWidget(self.profile_frame)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.menu_listwidget.setFont(font)
        self.menu_listwidget.setStyleSheet("QListView {\n"
"    padding-top:24px;\n"
"    border-radius: 20px;\n"
"    color: rgb(106, 106, 106);\n"
"    background-color: transparent;\n"
"}\n"
"QListView::item{\n"
"background-color: transparent;\n"
"height:40px;\n"
"padding-left:12px;\n"
"padding:12px;\n"
"}\n"
"QListView::item:hover {\n"
"    background-color: rgba(216, 216, 216, 50);\n"
"\n"
"}\n"
"QListView::item:selected {\n"
"    /*background-color: transparent;*/\n"
"    background-color: rgba(90, 216, 212,50);\n"
"    color: rgb(40, 92, 90);\n"
"border-left: 2px solid rgb(90, 216, 212)\n"
"\n"
"\n"
"}\n"
"")
        self.menu_listwidget.setIconSize(QtCore.QSize(24, 24))
        self.menu_listwidget.setObjectName("menu_listwidget")
        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/buttom/img/buttom/任天堂游戏_switch-nintendo.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        item.setIcon(icon)
        self.menu_listwidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/buttom/img/buttom/文件柜_file-cabinet.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        item.setIcon(icon1)
        self.menu_listwidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/buttom/img/buttom/设置配置_setting-config.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        item.setIcon(icon2)
        self.menu_listwidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/buttom/img/buttom/退出_logout.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        item.setIcon(icon3)
        self.menu_listwidget.addItem(item)
        self.verticalLayout_2.addWidget(self.menu_listwidget)
        self.switch_child_frame = QtWidgets.QFrame(self.profile_frame)
        self.switch_child_frame.setStyleSheet("QFrame{\n"
"    background-color: rgb(89, 217, 212);\n"
"    border-radius:20px;color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"")
        self.switch_child_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.switch_child_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.switch_child_frame.setObjectName("switch_child_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.switch_child_frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.click_to_label = QtWidgets.QLabel(self.switch_child_frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.click_to_label.setFont(font)
        self.click_to_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.click_to_label.setObjectName("click_to_label")
        self.verticalLayout.addWidget(self.click_to_label)
        self.switch_label = QtWidgets.QLabel(self.switch_child_frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.switch_label.setFont(font)
        self.switch_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.switch_label.setObjectName("switch_label")
        self.verticalLayout.addWidget(self.switch_label)
        self.kid_table = QtWidgets.QLabel(self.switch_child_frame)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.kid_table.setFont(font)
        self.kid_table.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.kid_table.setObjectName("kid_table")
        self.verticalLayout.addWidget(self.kid_table)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.switch_child_button = QtWidgets.QPushButton(self.switch_child_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.switch_child_button.sizePolicy().hasHeightForWidth())
        self.switch_child_button.setSizePolicy(sizePolicy)
        self.switch_child_button.setMinimumSize(QtCore.QSize(55, 55))
        self.switch_child_button.setMaximumSize(QtCore.QSize(55, 55))
        self.switch_child_button.setStyleSheet("image: url(:/buttom/img/buttom/切换_switch.svg);\n"
"border-radius:32px;\n"
"background-color: transparent;")
        self.switch_child_button.setText("")
        self.switch_child_button.setObjectName("switch_child_button")
        self.horizontalLayout.addWidget(self.switch_child_button)
        self.verticalLayout_2.addWidget(self.switch_child_frame)
        self.verticalLayout_2.setStretch(0, 1)
        self.horizontalLayout_7.addWidget(self.profile_frame)
        self.content_frame = QtWidgets.QVBoxLayout()
        self.content_frame.setSpacing(12)
        self.content_frame.setObjectName("content_frame")
        self.active_game_frame = QtWidgets.QFrame(self.central_frame)
        self.active_game_frame.setStyleSheet(".QFrame{\n"
"    background-color: rgba(255, 255, 255, 0);\n"
"    border-radius:20px;\n"
"}")
        self.active_game_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.active_game_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.active_game_frame.setObjectName("active_game_frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.active_game_frame)
        self.verticalLayout_3.setContentsMargins(-1, 24, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.active_game_title_label = QtWidgets.QLabel(self.active_game_frame)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.active_game_title_label.setFont(font)
        self.active_game_title_label.setStyleSheet("color: rgb(22, 54, 53)")
        self.active_game_title_label.setObjectName("active_game_title_label")
        self.verticalLayout_3.addWidget(self.active_game_title_label)
        self.active_game_layout = QtWidgets.QHBoxLayout()
        self.active_game_layout.setObjectName("active_game_layout")
        self.active_game_line = QtWidgets.QLineEdit(self.active_game_frame)
        self.active_game_line.setMinimumSize(QtCore.QSize(0, 32))
        self.active_game_line.setStyleSheet(".QLineEdit{\n"
"    background-color: rgba(255, 255, 255,0.8);\n"
"    border:0px solid red;\n"
"    border-radius:14px;\n"
"}")
        self.active_game_line.setInputMask("")
        self.active_game_line.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.active_game_line.setReadOnly(True)
        self.active_game_line.setObjectName("active_game_line")
        self.active_game_layout.addWidget(self.active_game_line)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.active_game_layout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.active_game_layout)
        self.content_frame.addWidget(self.active_game_frame)
        self.stackedWidget = QtWidgets.QStackedWidget(self.central_frame)
        self.stackedWidget.setObjectName("stackedWidget")
        self.game_page = QtWidgets.QWidget()
        self.game_page.setObjectName("game_page")
        self.game_scrollArea = QtWidgets.QScrollArea(self.game_page)
        self.game_scrollArea.setGeometry(QtCore.QRect(0, 0, 689, 434))
        self.game_scrollArea.setStyleSheet("QWidget{\n"
"border:none;\n"
"    background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.game_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.game_scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.game_scrollArea.setWidgetResizable(True)
        self.game_scrollArea.setObjectName("game_scrollArea")
        self.game_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.game_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 689, 434))
        self.game_scrollAreaWidgetContents.setObjectName("game_scrollAreaWidgetContents")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.game_scrollAreaWidgetContents)
        self.verticalLayout_13.setContentsMargins(36, 36, 124, 36)
        self.verticalLayout_13.setSpacing(24)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.game_scrollArea.setWidget(self.game_scrollAreaWidgetContents)
        self.stackedWidget.addWidget(self.game_page)
        self.library_page = QtWidgets.QWidget()
        self.library_page.setObjectName("library_page")
        self.library_scrollArea = QtWidgets.QScrollArea(self.library_page)
        self.library_scrollArea.setGeometry(QtCore.QRect(0, 0, 689, 434))
        self.library_scrollArea.setStyleSheet("QWidget{\n"
"border:none;\n"
"    background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.library_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.library_scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.library_scrollArea.setWidgetResizable(True)
        self.library_scrollArea.setObjectName("library_scrollArea")
        self.library_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.library_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 689, 434))
        self.library_scrollAreaWidgetContents.setObjectName("library_scrollAreaWidgetContents")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.library_scrollAreaWidgetContents)
        self.verticalLayout_14.setContentsMargins(36, 36, 124, 36)
        self.verticalLayout_14.setSpacing(24)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.library_scrollArea.setWidget(self.library_scrollAreaWidgetContents)
        self.stackedWidget.addWidget(self.library_page)
        self.setting_page = QtWidgets.QWidget()
        self.setting_page.setObjectName("setting_page")
        self.stackedWidget.addWidget(self.setting_page)
        self.content_frame.addWidget(self.stackedWidget)
        self.horizontalLayout_7.addLayout(self.content_frame)
        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 4)
        self.horizontalLayout_8.addWidget(self.central_frame)
        FamiOwl.setCentralWidget(self.centralwidget)

        self.retranslateUi(FamiOwl)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(FamiOwl)

    def retranslateUi(self, FamiOwl):
        _translate = QtCore.QCoreApplication.translate
        FamiOwl.setWindowTitle(_translate("FamiOwl", "FamiOwl Client"))
        self.parent_name_label.setText(_translate("FamiOwl", "Test"))
        self.child_name_label.setText(_translate("FamiOwl", "Child A"))
        __sortingEnabled = self.menu_listwidget.isSortingEnabled()
        self.menu_listwidget.setSortingEnabled(False)
        item = self.menu_listwidget.item(0)
        item.setText(_translate("FamiOwl", "Games"))
        item = self.menu_listwidget.item(1)
        item.setText(_translate("FamiOwl", "Library"))
        item = self.menu_listwidget.item(2)
        item.setText(_translate("FamiOwl", "Settings"))
        item = self.menu_listwidget.item(3)
        item.setText(_translate("FamiOwl", "Exit"))
        self.menu_listwidget.setSortingEnabled(__sortingEnabled)
        self.click_to_label.setText(_translate("FamiOwl", "Click To"))
        self.switch_label.setText(_translate("FamiOwl", "Switch"))
        self.kid_table.setText(_translate("FamiOwl", "Kid"))
        self.active_game_title_label.setText(_translate("FamiOwl", "Active Games"))
        self.active_game_line.setText(_translate("FamiOwl", "   Assassin\'s Creed: Brotherhood"))
