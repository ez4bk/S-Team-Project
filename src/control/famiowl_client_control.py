from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import QMainWindow

from config.client_info import config, write_to_json
from config.front_end.icon_path import list_widget_icons, switch_child_icon
from config.sql_query.client_query import show_top_game, show_inventory_game
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.pyqt_lib.message_box import message_info_box
from lib.pyqt_lib.query_handling import Worker
from src.control.famiowl_child_selection_control import FamiOwlChildSelectionWindow
from src.famiowl_client_window import Ui_FamiOwl
from src.model.fami_parent import FamiParent
from src.model.store_game import StoreGame

sql_utils = SqlUtils()


class FamiOwlClientWindow(QMainWindow, Ui_FamiOwl):
    def __init__(self, parent=None, fami_parent=None):
        super(FamiOwlClientWindow, self).__init__(parent)
        self.setupUi(self)
        self.child_selection_window = None
        self.start_x = None
        self.start_y = None
        self.threadpool = QThreadPool()
        self.game_timer = QtCore.QTimer(self)

        self.fami_parent = fami_parent
        self.kids = self.fami_parent.return_kids()
        # need a single parameter to store the current kid
        self.current_kid = None
        self.current_game = None
        self.top_games = []
        self.inventory_games = self.fami_parent.return_inventory()
        self.search_games = []

        self.parent_name_label.setText(fami_parent.return_parent_name())

        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.search_game_line.setAttribute(QtCore.Qt.WidgetAttribute.WA_MacShowFocusRect, 0)

        self.__define_icons()
        self.__define_menu_listwidget()
        self.__define_switch_child_button()
        self.__define_search_game_enter()
        self.game_timer.timeout.connect(self.__game_timer_timeout)
        self.__sync_profile()
        self.__get_game_local()

        self.menu_listwidget.setCurrentItem(self.menu_listwidget.itemAt(0, 0))
        self.stackedWidget.setCurrentWidget(self.inventory_page)

        if config['current_child'] is None:
            self.__to_child_selection_window()
        else:
            self.setupprofileicon()
            self.__switch_child()
        # self.__to_child_selection_window()

    def setupprofileicon(self):
        a = "src/resource/profile_icons/" + config['profile_icon'] + ".png"
        self.profile_image_widget.setStyleSheet("border-radius:32px;"
                                                "background-color: rgb(223, 223, 223);"
                                                "image: url(%s);" % a)

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
        self.kids = self.fami_parent.return_kids()
        self.child_selection_window = FamiOwlChildSelectionWindow(self, self.kids)
        if self.child_selection_window.isVisible():
            self.child_selection_window.hide()
        else:
            self.child_selection_window.show()

    def __define_switch_child_button(self):
        self.switch_child_button.clicked.connect(lambda: self.__to_child_selection_window())

    def __define_menu_listwidget(self):
        self.menu_listwidget.itemClicked.connect(lambda: self.__menu_select())

    def __menu_select(self):
        item = self.menu_listwidget.currentItem()
        widget_to_go = item.text()
        if widget_to_go == 'Inventory':
            self.__get_game_local()
            self.stackedWidget.setCurrentWidget(self.inventory_page)
        elif widget_to_go == 'Store':
            self.__get_game(1)
            self.stackedWidget.setCurrentWidget(self.store_page)
        elif widget_to_go == 'Settings':
            self.stackedWidget.setCurrentWidget(self.setting_page)
        elif widget_to_go == 'Exit':
            # TODO: Separate sign-out and exit
            config['signin_state'] = False
            write_to_json()
            self.fami_parent.sync_database()
            exit()

    def __get_game(self, flag=0):
        """
        :param flag: 0 for inventory, 1 for store, 2 for search result
        """
        worker = None
        try:
            if flag == 0:
                worker = Worker(self.__get_inventory_game_query, flag=flag)
            elif flag == 1:
                print(">>>>")
                worker = Worker(self.__get_top_game_query, flag=flag)
            elif flag == 2:
                self.stackedWidget.setCurrentWidget(self.search_page)
                worker = Worker(self.__get_search_game_query, flag=flag)
            worker.signals.result.connect(self.__game_thread_result)
            worker.signals.finished.connect(self.__game_thread_complete)
            self.threadpool.start(worker)
            self.menu_listwidget.setEnabled(False)
        except:
            pass

    def __get_game_local(self):
        self.inventory_games = self.fami_parent.return_inventory()
        self.__create_game_widgets(0)

    def __create_game_widgets(self, flag=0):
        layout = None
        game_list = []
        if flag == 0:
            game_list = self.inventory_games
            layout = self.inventory_list_layout
        elif flag == 1:
            game_list = self.top_games
            layout = self.store_list_layout
        elif flag == 2:
            game_list = self.search_games
            layout = self.search_list_layout

        for i in reversed(range(layout.count())):
            widget = layout.takeAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        if len(game_list) == 0:
            no_game_label = QtWidgets.QLabel()
            no_game_label.setText('No Games Found')
            no_game_label.setStyleSheet('background-color:transparent;'
                                        'color: black;')
            no_game_label.setObjectName("no_game_label")
            layout.addWidget(no_game_label)

        for i in range(len(game_list)):
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
            game_profile_button = QtWidgets.QPushButton(game_card)
            game_profile_button.setMinimumSize(QtCore.QSize(100, 100))
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum,
                                               QtWidgets.QSizePolicy.Policy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            game_profile_button.setSizePolicy(sizePolicy)
            game_cover = "src/resource/game_covers/" + game_list[i].return_game_name() + ".png"
            game_profile_button.setStyleSheet("image: url(%s);" % game_cover)
            game_profile_button.setObjectName("game_profile_widget_%s" % i)
            game_card_layout.addWidget(game_profile_button)
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
            game_name_label.setText(game_list[i].return_game_name())  # set game name
            game_info_layout.addWidget(game_name_label)
            game_info_label = QtWidgets.QLabel(game_card)
            font = QtGui.QFont()
            font.setBold(False)
            game_info_label.setFont(font)
            game_info_label.setStyleSheet("color: rgb(22, 54, 53)")
            game_info_label.setObjectName("game_info_label_%s" % i)
            game_info_label.setText("Game Info: " + game_list[i].return_game_descr())  # set game description
            game_info_layout.addWidget(game_info_label)
            if flag == 0 or (flag == 2 and game_list[i] in self.inventory_games):
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
            game_profile_button.clicked.connect(
                lambda _, f=flag, name=game_name_label.text(): self.__open_game(name, f))

            layout.addWidget(game_card)

    def __sync_profile(self):
        self.windowTitleChanged.connect(lambda: self.__switch_child())

    def __switch_child(self):
        self.__set_current_kid()
        self.child_name_label.setText(config['current_child'])
        self.threadpool.waitForDone(500)
        profile = self.current_kid.return_profile()
        try:
            a = "src/resource/profile_icons/" + profile + ".png"
            self.profile_image_widget.setStyleSheet("border-radius:32px;"
                                                    "background-color: rgb(223, 223, 223);"
                                                    "image: url(%s);" % a)
            self.time_left_int = self.current_kid.return_time_remaining()
            self.__update_gui()
        except Exception as e:
            assert True, e.__str__()
        # should call update playtime here

    # set current kid object for this window
    def __set_current_kid(self):
        kid_name = config['current_child']
        for kid in self.kids:
            if kid.return_kid_name() == kid_name:
                self.current_kid = kid
        self.current_kid.init_playtime()

    def __get_top_game_query(self, flag=0):
        res = None
        games = []

        try:
            res = sql_utils.sql_exec(show_top_game.format(10), 1)
        except Exception as e:
            return 'Fetch game store failed!'
        if res is None or res == []:
            return "No games available!"
        try:
            for a in res:
                game = StoreGame(a[0], a[1], a[2], a[3], a[4], a[5])
                games.append(game)
            self.top_games = games
            return flag
        except Exception:
            return "Game initialization failed!"

    def __get_kids(self):
        try:
            worker = Worker(self.__get_kids_query)
            worker.signals.result.connect(self.__kids_thread_result)
            worker.signals.finished.connect(self.__kids_thread_complete)
            self.threadpool.start(worker)
            self.setEnabled(False)
        except:
            pass

    def __get_kids_query(self):
        return self.fami_parent.get_kids_info_query()

    def __get_inventory_game_query(self, flag=0):
        res = None
        games = []
        try:
            res = sql_utils.sql_exec(show_inventory_game.format(self.fami_parent.return_parent_id()))
        except Exception as e:
            return 'Fetch game store failed!'
        if res is None or res == []:
            self.inventory_games = games
            self.fami_parent.set_inventory(games)
            return flag

        try:
            for a in res:
                game = StoreGame(a[0], a[1], a[2], a[3], a[4], a[5])
                games.append(game)
            self.inventory_games = games
            self.fami_parent.set_inventory(games)
            return flag
        except Exception:
            return "Game initialization failed!"

    def __game_thread_result(self, result):
        if result is not str:
            # self.fami_parent.set_inventory(self.inventory_games)
            self.__create_game_widgets(result)
        else:
            message_info_box(self, str(result))

    def __game_thread_complete(self):
        self.menu_listwidget.setEnabled(True)

    def __kids_thread_result(self, result):
        if isinstance(result, FamiParent):
            self.fami_parent = result
        else:
            message_info_box(self, str(result))

    def __kids_thread_complete(self):
        self.setEnabled(True)

    def __open_game(self, game_name, flag=0):
        games = None

        if flag == 0:
            games = self.inventory_games
        elif flag == 1:
            games = self.top_games
        else:
            pass
        for game in games:
            if game.return_game_name() == game_name:
                #     try:
                #         if (flag != 0) and (game not in self.inventory_games):
                #             self.inventory_games.append(game)
                if flag == 0:
                    if self.current_kid.return_time_remaining() < 1:
                        message_info_box(self, 'No more time to play!')
                        return
                    self.__start_game_timer()
                    game.run_game(self.fami_parent)
                    self.current_game = game
                    worker = Worker(self.__run_game_thread)
                    worker.signals.result.connect(self.__run_game_thread_result)
                    worker.signals.finished.connect(self.__run_game_thread_complete)
                    self.threadpool.start(worker)
                else:
                    self.fami_parent = game.run_game(self.fami_parent)

    def __run_game_thread(self):
        # self.fami_parent = game.run_game(self.fami_parent)
        while self.current_game.proc.poll() is None:
            print('pass')
        print('finished')

    def __run_game_thread_result(self, result):
        pass

    def __run_game_thread_complete(self):
        self.game_timer.stop()
        self.current_game = None
        self.current_kid.set_time_remaining(self.time_left_int)

    def __define_search_game_enter(self):
        self.search_game_line.returnPressed.connect(lambda: self.__get_game(2))

    def __get_search_game_query(self, flag=0):
        keyword = self.search_game_line.text()
        res = None
        games = []
        for game in self.top_games:
            if keyword.lower() in game.return_game_name().lower():
                games.append(game)

        self.search_games = games
        return True

    def __start_game_timer(self):
        self.time_left_int = self.current_kid.return_time_remaining()
        # self.game_timer.setInterval(1000)
        self.game_timer.start(1000)

    def __game_timer_timeout(self):
        self.time_left_int -= 1

        if self.time_left_int == 0:
            if self.current_game is not None:
                self.current_game.stop()
            message_info_box(self, 'Game Time Over!')
        self.__update_gui()

    @staticmethod
    def __secs_to_minsec(secs: int):
        mins = secs // 60
        hours = mins // 60
        mins = mins % 60
        secs = secs % 60
        minsec = f'{hours:02}:{mins:02}:{secs:02}'
        return minsec

    def __update_gui(self):
        minsec = self.__secs_to_minsec(self.time_left_int)
        self.game_timer_lcd.display(minsec)
