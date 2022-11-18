import os
import subprocess

from config.project_info import DOWNLOAD_DIR
from src.model.game import Game


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

    def __str__(self):
        return ""
