from lib.base_lib.sql.sql_utils import SqlUtils

sql_utils = SqlUtils()


class FamiParent:

    def __init__(self, parent_id, parent_name, parent_profile='', kids=None, inventory=None):
        self.__parent_id = parent_id
        self.__parent_name = parent_name
        self.__parent_profile = parent_profile
        self.__kids = kids
        self.__game = None
        self.__inventory = inventory

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
        self.parent_name = name
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
