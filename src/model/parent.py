class Parent:

    def __init__(self, parent_id, parent_name, parent_profile='', children=None):
        self.__parent_id = parent_id
        self.__parent_name = parent_name
        self.__parent_profile = parent_profile
        self.__children = children

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
