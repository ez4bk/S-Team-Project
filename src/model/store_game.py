import os
import subprocess

from config.project_info import DOWNLOAD_DIR, VM_SRC_DIR
from lib.base_lib.sftp_utils.sftp_utils import SftpUtils
from lib.base_lib.sql.sql_utils import SqlUtils
from src.model.game import Game

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
        # self.add_to_inventory(fami_parent)
        self.download()
        path = os.path.join(DOWNLOAD_DIR, self.return_game_name())
        completed_process = subprocess.run(["python3", path + '.py'])
        print(completed_process.returncode)
        # completed_process.returncode

    def add_to_inventory(self, fami_parent):
        inventory = fami_parent.return_inventory()
        for game in inventory:
            if game.return_game_id() == self.return_game_id():
                print(fami_parent.return_inventory())
                raise "Game already in inventory"
            else:
                fami_parent.add_to_inventory(self)
        return fami_parent

    def download(self):
        name = self.return_game_name() + ".py"
        download_dir_path = self.return_path()
        sftp_utils.sftp_download(download_dir_path, name)

    def rate(self):
        res = SqlUtils.sql_exec()
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
