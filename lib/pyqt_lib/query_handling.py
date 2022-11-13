from PyQt6.QtCore import QObject, pyqtSignal

from config.client_info import config, write_to_json
from config.sql_query.account_query import parent_signin, parent_id_check, parent_signup, kids_select
from config.sql_query.client_query import show_top_game, add_to_inventory, exist_game_check
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.base_lib.utils.aes_pass import AESCipher
from src.model.child import Child

sql_utils = SqlUtils()
aes_cipher = AESCipher()


class QueryHandling(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, **kwargs):
        QObject.__init__(self)
        self.kwargs = dict(kwargs)

    def handle_signin_query(self):
        res = None
        id_input = self.kwargs.get('id_input')
        pwd_input = self.kwargs.get('pwd_input')
        try:
            res = sql_utils.sql_exec(parent_id_check.format(id_input), 1)[0][0]
        except Exception as e:
            self.error.emit('Fetch parent info failed!')
            return

        if res is None:
            self.error.emit("Fetch parent info failed!")
            return
        elif res == 0:
            self.error.emit("User does not exist")
            return

        try:
            res = sql_utils.sql_exec(parent_signin.format(id_input), 1)[0]
        except Exception as e:
            self.error.emit('Fetch parent info failed!')
            return

        if not verify_pwd(pwd_input, res[1]):
            self.error.emit("Password Incorrect!")
            return
        else:
            config['parent_name'] = res[0]
            config['parent_pwd'] = res[1]
            config['signin_state'] = True
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
            self.error.emit('Fetch database failed!')
            return
        if res == 1:
            self.error.emit("E-mail already registered!")
            return
        else:
            try:
                signup_query = parent_signup.format(user_id, user_name, pwd)
                sql_utils.sql_exec(signup_query, 0)
                self.finished.emit()
            except Exception as e:
                self.error.emit('Sign up failed!')
                return

    def handle_show_top_game_query(self):
        from src.model.store_game import StoreGame
        res = None
        try:
            res = sql_utils.sql_exec(show_top_game.format(10), 1)
        except Exception as e:
            self.error.emit('Fetch game stroe failed!')
            return
        if res is None:
            self.error.emit("No games available!")
            return
        games = []

        try:
            for a in res:
                game = StoreGame(a[0], a[1], a[2], a[3], a[4], a[5])
                games.append(game)
            self.kwargs['ui'].top_games = games
            self.finished.emit()
        except Exception:
            self.error.emit("Game initialization failed!")
            return

    def handle_add_to_inventory_query(self):
        game_id = self.kwargs['game_id']
        parent_id = config['parent_id']
        try:
            res = sql_utils.sql_exec(exist_game_check.format(parent_id, game_id), 1)[0][0]
        except Exception as e:
            self.error.emit('Fetch database failed!')
            return
        if res == 1:
            self.error.emit("Game already in the inventory!")
            return
        else:
            try:
                sql_utils.sql_exec(add_to_inventory.format(parent_id, game_id), 0)
                self.finished.emit()
            except Exception as e:
                self.error.emit('Fetch database failed!')
                return

    def handle_kids_profile(self):
        res = None
        try:
            res = sql_utils.sql_exec(kids_select.format(config['parent_id']))
        except Exception as e:
            self.error.emit("Could not fetch kids info")
            return

        if res is None:
            self.error.emit("Could not fetch kids info")
            return
        children = []
        try:
            for a in res:
                child = Child(a[0], a[1], self.kwargs['ui'].parent_obj, a[3], a[4])
                children.append(child)
            self.kwargs['ui'].kids = children
            self.finished.emit()
        except Exception as e:
            self.error.emit('Fetch children info failed!')
            return


def verify_pwd(user_input, pwd):
    try:
        if aes_cipher.decrypt_main(pwd) == user_input:
            return True
        else:
            return False
    except Exception as e:
        assert False, e
