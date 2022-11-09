from PyQt6.QtCore import QObject, pyqtSignal

from config.client_info import config, write_to_json
from config.sql_query.account_query import parent_signin, parent_id_check, parent_signup
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.pyqt_lib.message_box import message_info_box

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
            message_info_box(self, e.__str__())
        if res == 0:
            config['parent_id'] = None
            write_to_json()
            self.finished.emit()
        else:
            try:
                res = sql_utils.sql_exec(parent_signin.format(config['parent_id']), 1)[0]
            except Exception as e:
                message_info_box(self, e.__str__())

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
            message_info_box(None, e.__str__())
        if res == 1:
            message_info_box(None, "E-mail already registered!")
            self.finished.emit()
        else:
            try:
                signup_query = parent_signup.format(user_id, user_name, pwd)
                sql_utils.sql_exec(signup_query, 0)
            except Exception as e:
                message_info_box(ui, e.__str__())
            self.finished.emit()
