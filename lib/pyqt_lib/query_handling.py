from PyQt6.QtCore import QObject, pyqtSignal

from config.client_info import config, write_to_json
from config.sql_query.account_query import parent_signin, parent_id_check, parent_signup
from config.sql_query.client_query import show_top_game, add_to_inventory, exist_game_check
from lib.base_lib.sql.sql_utils import SqlUtils

sql_utils = SqlUtils()


class QueryHandling(QObject):
    finished = pyqtSignal()

    def __init__(self, **kwargs):
        QObject.__init__(self)
        self.kwargs = dict(kwargs)

    def handle_signin_query(self):
        res = None
        try:
            res = sql_utils.sql_exec(parent_id_check.format(config['parent_id']), 1)[0][0]
        except Exception as e:
            assert False, e
        if res == 0:
            config['parent_id'] = None
            write_to_json()
            self.finished.emit()
        else:
            try:
                res = sql_utils.sql_exec(parent_signin.format(config['parent_id']), 1)[0]
            except Exception as e:
                assert False, e

            if res is not None:
                config['parent_name'] = res[0]
                config['parent_pwd'] = res[1]
                write_to_json()
            self.finished.emit()

    def handle_signup_query(self):
        res = None
        user_id = self.kwargs['user_id']
        user_name = self.kwargs['user_name']
        pwd = self.kwargs['pwd']
        ui = self.kwargs['ui']
        try:
            res = sql_utils.sql_exec(parent_id_check.format(user_id), 1)[0][0]
        except Exception as e:
            assert False, e
        if res == 1:
            assert False, "E-mail already registered!"
            self.finished.emit()
        else:
            try:
                signup_query = parent_signup.format(user_id, user_name, pwd)
                sql_utils.sql_exec(signup_query, 0)
            except Exception as e:
                assert False, e
            self.finished.emit()

    def handle_show_top_game_query(self):
        from src.model.store_game import StoreGame
        res = None
        try:
            res = sql_utils.sql_exec(show_top_game.format(10), 1)
        except Exception as e:
            assert False, e
        assert res is not None, "No games available!"
        games = []

        try:
            for a in res:
                game = StoreGame(a[0], a[1], a[2], a[3], a[4], a[5])
                games.append(game)
            self.kwargs['ui'].top_games = games
        except Exception:
            assert False, "Game initialization failed!"
        self.finished.emit()

    def handle_add_to_inventory_query(self):
        game_id = self.kwargs['game_id']
        parent_id = config['parent_id']
        try:
            res = sql_utils.sql_exec(exist_game_check.format(parent_id, game_id), 1)[0][0]
        except Exception as e:
            assert False, e
        if res == 1:
            assert False, "Game already in the inventory!"
        else:
            try:
                sql_utils.sql_exec(add_to_inventory.format(parent_id, game_id), 0)
            except Exception as e:
                assert False, e
            self.finished.emit()
