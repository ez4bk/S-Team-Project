import os.path

from config.project_info import DOWNLOAD_DIR
from config.sql_query.game_query import add_likes
from lib.base_lib.sftp_utils.sftp_utils import SftpUtils
from lib.base_lib.sql.sql_utils import SqlUtils
from src.model.game import Game
from src.model.inventory_game import InventoryGame

sql_utils = SqlUtils()
sftp_utils = SftpUtils()


class StoreGame(Game):

    # Will be initialized by famiowl_client_control
    # client_control will pass
    def __init__(self, game_id, game_name, cover_img, path, game_description, likes_count):
        super().__init__(game_id, game_name, cover_img, game_description)
        self.__path = path
        self.__likes_count = int(likes_count)
        self.__filesize = ""

    def run_game(self, fami_parent):
        path = self.download()
        parent_invent = fami_parent.return_inventory()
        if self not in parent_invent:
            fami_parent = self.add_to_inventory(fami_parent, path)
        else:
            return 'Game already in inventory!'
        return fami_parent

    # add store game to inventory
    def add_to_inventory(self, fami_parent, local_path):
        inventory = fami_parent.return_inventory()
        if inventory is not []:
            for game in inventory:
                if game.return_game_id() == self.return_game_id():
                    return fami_parent
        inventory_game = InventoryGame(self, fami_parent, local_path)
        fami_parent.add_to_inventory(inventory_game)
        return fami_parent

    # download game
    def download(self):
        name = self.return_game_name() + ".py"
        download_dir_path = self.__path
        full_path = os.path.join(DOWNLOAD_DIR, name)
        if os.path.exists(full_path):
            return full_path
        else:
            sftp_utils.sftp_download(download_dir_path, name)
            return full_path

    # increase like count by 1
    def add_like(self):
        self.__likes_count += 1

    # decrease like count by 1
    def remove_like(self):
        self.__likes_count -= 1

    def return_path(self):
        return str(self.__path)

    def return_like_count(self):
        return str(self.__likes_count)

    def return_filesize(self):
        return str(self.__filesize)

    def sync_likes(self):
        sql_utils.sql_exec(add_likes.format(self.return_game_id()), 0)
