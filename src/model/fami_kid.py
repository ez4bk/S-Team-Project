class FamiKid:
    def __init__(self, kid_id, kid_name, parent, profile, time_limit):
        self.__kid_id = kid_id
        self.__kid_name = kid_name
        self.__profile = profile
        self.__parent = parent
        self.__time_limit = time_limit

    def return_kid_id(self):
        return str(self.__kid_id)

    def return_kid_name(self):
        return str(self.__kid_name)

    def return_parent_id(self):
        return str(self.__parent.return_kid_id())

    def return_profile(self):
        return str(self.__profile)

    def return_time_limit(self):
        return int(self.__time_limit)
