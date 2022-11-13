from config.sql_query.client_query import show_inventory_game
from lib.base_lib.sql.sql_utils import SqlUtils

sql_utils = SqlUtils()


class Parent:

    def __init__(self, parent_id, parent_name, parent_profile='', children=None):
        self.__parent_id = parent_id
        self.__parent_name = parent_name
        self.__parent_profile = parent_profile
        self.__children = children
        self.__game = None

    def __get_inventory(self):
        pass

    def __get_inventory_query(self):
        res = None
        try:
            res = sql_utils.sql_exec(show_inventory_game.format(self.__parent_id), 1)
        except:
            return "Fetch game inventory failed!"

        if res is None:
            return "Fetch game inventory failed!"

        if res == 0:
            return 0

    def add_child(self):
        pass

    def change_name(self, name):
        self.parent_name = name
        # TODO: change name query

    def init_children(self, children=None):
        self.__children = children

    def return_parent_id(self):
        return self.return_parent_id

    def return_parent_name(self):
        return str(self.__parent_name)

    def return_parent_profile(self):
        return str(self.__parent_profile)

    def return_children(self):
        return self.__children
