from config.client_info import config, write_to_json
from config.sql_query.account_query import parent_id_check, parent_signin, kids_select
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.base_lib.utils.aes_pass import AESCipher
from src.model.fami_kid import FamiKid

sql_utils = SqlUtils()
aes_cipher = AESCipher()


class FamiParent:

    def __init__(self, parent_id='', parent_name='', parent_profile='', kids=None, inventory=None):
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
                kid = FamiKid(a[0], a[1], self, a[3], a[4])
                kids_list.append(kid)
            self.__kids = kids_list
            return self
        except Exception as e:
            return 'Fetch kids_list info failed!'

    def sync_database(self):
        pass

    def set_kids(self, kids):
        self.__kids = kids

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
        # TODO: change name query

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
