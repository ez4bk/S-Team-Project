import os
import subprocess
import sys

from config.client_info import config
from config.project_info import DOWNLOAD_DIR
from config.sql_query.game_query import time_record_update, time_record_check, get_kid_id, add_likes
from lib.base_lib.sql.sql_utils import SqlUtils
from src.model.game import Game

sql_utils = SqlUtils()


class InventoryGame(Game):
    def __init__(self, game, fami_parent, local_path=''):
        super().__init__(game.return_game_id(), game.return_game_name(), game.return_cover_img(),
                         game.return_game_descr())
        self.store_game = game
        self.__fami_parent = fami_parent
        if local_path == '':
            self.__local_path = os.path.join(DOWNLOAD_DIR, self.return_game_name())
        else:
            self.__local_path = local_path
        self.__liked = False
        self.proc = None
        self.pid = -1

    def run_game(self, fami_parent):
        path = os.path.join(DOWNLOAD_DIR, self.return_game_name())
        path = path.replace(' ', '\ ')
        python_cmd = 'python'
        # time.sleep(5)
        # return fami_parent
        if sys.version_info >= (3, 0):
            python_cmd = 'python3'
        cmd = '%s %s.py' % (python_cmd, path)
        try:
            # completed_process = subprocess.run([python_cmd, path + '.py'])
            self.proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
            self.pid = self.proc.pid
            return fami_parent
        except:
            pass
        return fami_parent

    def stop(self):
        # os.killpg(self.pid, signal.SIGKILL)
        self.proc.kill()

    def return_likes(self):
        self.store_game.return_likes()

    def hit_like(self):
        self.__liked = True
        self.store_game.add_like()

    def hit_unlike(self):
        self.__liked = False
        self.store_game.remove_like()

    def return_liked(self):
        return self.__liked

    def sync_likes(self):
        if self.__liked:
            SqlUtils.sql_exec(add_likes.format(self.return_game_id()), 0)

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

    def return_store_game(self):
        return self.store_game

    def __str__(self):
        return ""
