from datetime import date

from config.sql_query.account_query import update_last_played, update_time_played_today
from lib.base_lib.sql.sql_utils import SqlUtils

sql_utils = SqlUtils()


class FamiKid:
    def __init__(self, kid_id, kid_name, parent, profile, time_limit, last_played, time_played_today):
        self.__kid_id = kid_id
        self.__kid_name = kid_name
        self.__profile = profile
        self.__parent = parent
        self.__time_limit = time_limit * 60
        self.__last_played = last_played
        if last_played != date.today():
            self.__time_played_today = 0
        else:
            self.__time_played_today = time_played_today * 60
        self.__time_remaining = self.__time_limit - self.__time_played_today

    def sync_database(self):
        self.sync_playtime()

    def sync_playtime(self):
        time_played_minutes = round(self.__time_played_today / 60)
        try:
            sql_utils.sql_exec(update_time_played_today.format(time_played_minutes, self.__kid_id), 0)
        except Exception as e:
            return 'Update playtime failed.'

    def init_playtime(self):
        today_date = date.today()
        last_played_indb = self.__last_played
        kid_id = self.__kid_id
        if last_played_indb == today_date:
            return
        else:
            try:
                sql_utils.sql_exec(update_last_played.format(today_date, kid_id), 0)
                sql_utils.sql_exec(update_time_played_today.format(0, kid_id), 0)
            except Exception as e:
                return 'Update playtime failed. '

    def return_kid_id(self):
        return str(self.__kid_id)

    def return_kid_name(self):
        return str(self.__kid_name)

    def return_parent_id(self):
        return str(self.__parent.return_parent_id())

    def return_profile(self):
        return str(self.__profile)

    def return_time_limit(self):
        return int(self.__time_limit)

    def return_last_played(self):
        return date(self.__last_played)

    def return_time_played_today(self):
        return int(self.__time_played_today)

    def return_time_remaining(self):
        return int(self.__time_remaining)

    def set_time_remaining(self, time_remaining):
        self.__time_remaining = time_remaining
        self.__time_played_today = self.__time_limit - self.__time_remaining

    def set_time_played_today(self, time_played_today):
        self.__time_played_today = time_played_today

    def set_last_played(self, last_played):
        self.__last_played = last_played
