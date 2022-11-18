import os
import subprocess

from config.project_info import DOWNLOAD_DIR
from src.model.game import Game

from lib.base_lib.sql.sql_utils import SqlUtils
from config.sql_query.game_query import time_record_update,time_record_check

sql_utils = SqlUtils()


class InventoryGame(Game):
    def __init__(self, game, fami_parent, local_path=''):
        super().__init__(game.return_game_id(), game.return_game_name(), game.return_cover_img(),
                         game.return_game_descr())
        self.__fami_parent = fami_parent
        if local_path == '':
            self.__local_path = os.path.join(DOWNLOAD_DIR, self.return_game_name())
        else:
            self.__local_path = local_path

    def run_game(self, fami_parent):
        path = os.path.join(DOWNLOAD_DIR, self.return_game_name())
        try:
            completed_process = subprocess.run(["python3", path + '.py'])
        except:
            pass
        return fami_parent

    def stop(self):
        return 0

    def monitor(self):
        return 0

    def delete(self):
        return 0

# Wendi: get kid id from parents table, use kid id to find
    def accumulate_playtime(self):
#       kid_id = sql_utils.sql_exec
#        record_exist = sql_utils.sql_exec(time_record_check.format(kid_id, self.return_game_id()),1)[1][1]
        return 0
    def __str__(self):
        return ""
