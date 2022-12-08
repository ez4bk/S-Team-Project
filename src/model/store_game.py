import os.path

from config.project_info import VM_SRC_DIR, DOWNLOAD_DIR
from config.sql_query.game_query import get_ratings
from lib.base_lib.sftp_utils.sftp_utils import SftpUtils
from lib.base_lib.sql.sql_utils import SqlUtils
from src.model.game import Game
from src.model.inventory_game import InventoryGame

sql_utils = SqlUtils()
sftp_utils = SftpUtils()


class StoreGame(Game):
    def __init__(self, game_id, game_name, cover_img, path, game_description, sales):
        super().__init__(game_id, game_name, cover_img, game_description)
        self.__path = path
        self.__sales = sales
        self.__rate = ""
        self.__filesize = ""

    def run_game(self, fami_parent):
        path = self.download()
        if self not in fami_parent.return_inventory():
            fami_parent = self.add_to_inventory(fami_parent, path)
        else:
            pass
        return fami_parent

    def add_to_inventory(self, fami_parent, local_path):
        inventory = fami_parent.return_inventory()
        if inventory is not []:
            for game in inventory:
                if game.return_game_id() == self.return_game_id():
                    return fami_parent
        inventory_game = InventoryGame(self, fami_parent, local_path)
        fami_parent.add_to_inventory(inventory_game)
        return fami_parent

    def download(self):
        name = self.return_game_name() + ".py"
        download_dir_path = self.__path
        full_path = os.path.join(DOWNLOAD_DIR, name)
        print(full_path)
        if os.path.exists(full_path):
            return full_path
        else:
            sftp_utils.sftp_download(download_dir_path, name)
            return full_path

    def rate(self):
        res = SqlUtils.sql_exec(get_ratings.format(self.return_game_id()), 1)[0]
        return res

    def __str__(self):
        return ""

    def return_path(self):
        return str(self.__path)

    def return_sales(self):
        return str(self.__sales)

    def return_rate(self):
        return str(self.__rate)

    def return_filesize(self):
        return str(self.__filesize)


if __name__ == '__main__':
    a = StoreGame('1', 'Snake', 'img', VM_SRC_DIR + '/snake.py', 'desc', 'sales')
    print(a.run_game(None))
