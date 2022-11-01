from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow

from src.famiowl_client_window import Ui_FamiOwl


class FamiOwlClientWindow(QMainWindow, Ui_FamiOwl):
    def __init__(self, parent=None):
        super(FamiOwlClientWindow, self).__init__(parent)
        self.setupUi(self)

        self.start_x = None
        self.start_y = None
        self.anim = None

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.active_game_line.setAttribute(QtCore.Qt.WidgetAttribute.WA_MacShowFocusRect, 0)
        self.create_game_widgets()

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

    def create_game_widgets(self):
        for i in range(5):
            object = QtWidgets.QWidget()
            object.setMinimumSize(QtCore.QSize(0, 121))
            object.setMaximumSize(QtCore.QSize(16777215, 121))
            object.setStyleSheet(".QWidget{\n"
                                 "    background-color: qlineargradient(x1:0, y0:0, x2:1, y2:0,stop:0 rgb(234, 249, 253), stop:1 rgb(155, 230, 237));\n"
                                 "    border-radius:20px;\n"
                                 "    color: rgb(255, 255, 255);\n"
                                 "}\n"
                                 "\n"
                                 "")
            object.setObjectName("game_widget_0%s" % i)
            h_layout = QtWidgets.QHBoxLayout(object)
            h_layout.setContentsMargins(24, 24, 24, 24)
            h_layout.setSpacing(24)
            h_layout.setObjectName("horizontalLayout_5%s" % i)
            p_widget = QtWidgets.QWidget(object)
            p_widget.setMaximumSize(QtCore.QSize(100, 16777215))
            p_widget.setStyleSheet("image: url(:/svg/img/button_png/image.jpg);")
            p_widget.setObjectName("widget_5%s" % i)
            h_layout.addWidget(p_widget)
            i_layout = QtWidgets.QVBoxLayout()
            i_layout.setSpacing(2)
            i_layout.setObjectName("game_info_layout_0%s" % i)
            n_label = QtWidgets.QLabel(object)
            font = QtGui.QFont()
            font.setPointSize(16)
            font.setBold(True)
            n_label.setFont(font)
            n_label.setStyleSheet("color: rgb(22, 54, 53)")
            n_label.setObjectName("game_name_0%s" % i)
            n_label.setText("Game #%s" % i)
            i_layout.addWidget(n_label)
            i_label = QtWidgets.QLabel(object)
            font = QtGui.QFont()
            font.setBold(False)
            i_label.setFont(font)
            i_label.setStyleSheet("color: rgb(22, 54, 53)")
            i_label.setObjectName("game_info_0")
            i_label.setText("Game Info #%s" % i)
            i_layout.addWidget(i_label)
            bar = QtWidgets.QProgressBar(object)
            bar.setStyleSheet("QProgressBar::chunk {\n"
                              "        border-top-left-radius:8px;\n"
                              "border-bottom-left-radius:8px;\n"
                              "    background-color: rgb(103, 216, 217)\n"
                              "}\n"
                              "QProgressBar{\n"
                              "border-radius:8px;\n"
                              "background-color: rgb(223, 223, 223);\n"
                              "}\n"
                              "")
            bar.setProperty("value", 60)
            bar.setTextVisible(False)
            bar.setObjectName("game_limit_bar_0%s" % i)
            i_layout.addWidget(bar)
            h_layout.addLayout(i_layout)
            h_layout.setStretch(0, 1)

            self.verticalLayout_13.addWidget(object)
