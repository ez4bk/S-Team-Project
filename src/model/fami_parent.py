from config.client_info import config, write_to_json
from config.sql_query.account_query import parent_id_check, parent_signin, kids_select, show_parent_inventory, add_kid
from config.sql_query.client_query import add_to_inventory, show_inventory_game
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.base_lib.utils.aes_pass import AESCipher
from src.model.fami_kid import FamiKid

sql_utils = SqlUtils()
aes_cipher = AESCipher()


class FamiParent:

    def __init__(self, parent_id='', parent_name='', parent_profile='', kids=[], inventory=[]):
        self.__parent_id = parent_id
        self.__parent_name = parent_name
        self.__parent_profile = parent_profile
        self.__kids = kids
        self.__inventory = inventory

    def get_parent_info_query(self, id_input, pwd_input):
        try:
            res = sql_utils.sql_exec(parent_id_check.format(id_input), 1)[0][0]
        except Exception as e:
            return 'Fetch parent info failed!'

        if res is None:
            return "Fetch parent info failed!"
        elif res == 0:
            return "User does not exist"

        try:
            res = sql_utils.sql_exec(parent_signin.format(id_input), 1)[0]
        except Exception as e:
            return 'Fetch parent info failed!'

        if not self.__verify_pwd(pwd_input, res[1]):
            return "Password Incorrect!"
        else:
            self.__parent_id = id_input
            self.__parent_name = res[0]
            config['parent_id'] = id_input
            config['parent_name'] = res[0]
            config['parent_pwd'] = res[1]
            config['signin_state'] = True
            write_to_json()
            return self

    def get_kids_info_query(self):
        res = None
        kids_list = []
        try:
            res = sql_utils.sql_exec(kids_select.format(self.__parent_id))
        except Exception as e:
            return "Could not fetch kids info"

        if res is None or res == []:
            self.__kids = kids_list
            return self

        try:
            for a in res:
                kid = FamiKid(a[0], a[1], self, a[3], a[4], a[5], a[6])
                kids_list.append(kid)
            self.__kids = kids_list
            return self
        except Exception as e:
            return 'Fetch kids_list info failed!'

    def get_inventory_query(self):
        res = None
        games = []
        id_res = []
        try:
            res = sql_utils.sql_exec(show_inventory_game.format(self.__parent_id))
        except Exception as e:
            return 'Fetch game store failed!'

        if res is None or res == []:
            self.__inventory = games
            return id_res

        for a in res:
            id_res.append(a[2])

        return id_res

    def sync_database(self):
        self.__sync_kids()
        self.__sync_inventory()

    def __sync_kids(self):
        existing_kids = []
        res = sql_utils.sql_exec(kids_select.format(self.__parent_id))
        for kid in res:
            existing_kids.append(kid[1])
        for kid in self.__kids:
            if kid.return_kid_name() not in existing_kids:
                sql_utils.sql_exec(
                    add_kid.format(kid.return_kid_name(), kid.return_parent_id(), kid.return_profile(),
                                   kid.return_time_limit()), 0)
        for kid in self.__kids:
            kid.sync_database()

    def __sync_inventory(self):
        existing_games = []
        res = sql_utils.sql_exec(show_parent_inventory.format(self.__parent_id))
        for game in res:
            existing_games.append(int(game[2]))
        for game in self.__inventory:
            if int(game.return_game_id()) not in existing_games:
                sql_utils.sql_exec(
                    add_to_inventory.format(self.__parent_id, game.return_game_id()), 0)
            if game.return_liked():
                game.sync_database()

    def set_inventory(self, inventory):
        self.__inventory = inventory

    def add_to_inventory(self, game):
        self.__inventory.append(game)

    def __get_inventory(self):
        return self.__inventory

    def add_kid(self, kid):
        self.__kids.append(kid)

    def change_name(self, name):
        self.__parent_name = name

    def return_parent_id(self):
        return str(self.__parent_id)

    def return_parent_name(self):
        return str(self.__parent_name)

    def return_parent_profile(self):
        return str(self.__parent_profile)

    def return_kids(self):
        return self.__kids

    def return_inventory(self):
        return self.__inventory

    @staticmethod
    def __verify_pwd(user_input, pwd):
        try:
            if aes_cipher.decrypt_main(pwd) == user_input:
                return True
            else:
                return False
        except Exception as e:
            assert False, e
