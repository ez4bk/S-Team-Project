import os
import subprocess

from config.client_info import config
from config.project_info import DOWNLOAD_DIR
from config.sql_query.game_query import time_record_update, time_record_check, get_kid_id
from lib.base_lib.sql.sql_utils import SqlUtils
from src.model.game import Game

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
        # print(process_listen.find_process_by_name('snake'))
        try:
            completed_process = subprocess.run(["python3", path + '.py'])
            # subprocess.call(r'python3 %s.py' % path)
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
    # time_played: the time this kid spent on this game this time opening the game
    def accumulate_playtime(self, time_played):
        kid_name = config.get['current_child']
        parent_id = config.get['parent_id']
        game_id = self.return_game_id()
        kid_id = sql_utils.sql_exec(get_kid_id.format(kid_name, parent_id), 1)[1][1]
        record_exist = sql_utils.sql_exec(time_record_check.format(kid_id, game_id), 1)[1][1]
        if record_exist:
            sql_utils.sql_exec(time_record_update.format(kid_id, game_id, time_played), 0)

    def __str__(self):
        return ""
