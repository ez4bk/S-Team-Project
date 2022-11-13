class Child:
    def __init__(self, child_id, child_name, parent, profile, time_limit):
        self.__child_id = child_id
        self.__child_name = child_name
        self.__profile = profile
        self.__parent = parent
        self.__time_limit = time_limit

    def return_child_id(self):
        return str(self.__child_id)

    def return_child_name(self):
        return str(self.__child_name)

    def return_parent_id(self):
        return str(self.__parent.return_child_id())

    def return_profile(self):
        return str(self.__profile)

    def return_time_limit(self):
        return int(self.__time_limit)
