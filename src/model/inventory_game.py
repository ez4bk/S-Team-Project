import os

from config.project_info import DOWNLOAD_DIR
from src.model.game import Game


class InventoryGame(Game):
    def __init__(self, game, fami_parent, local_path=''):
        super().__init__(game.return_game_id(), game.return_game_name())
        self.__fami_parent = fami_parent
        if local_path == '':
            self.__local_path = os.path.join(DOWNLOAD_DIR, self.return_game_name())
        else:
            self.__local_path = local_path

    def run_game(self, fami_parent):
        return 0

    def stop(self):
        return 0

    def monitor(self):
        return 0

    def delete(self):
        return 0

    def __str__(self):
        return ""
