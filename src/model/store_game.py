from src.model.game import Game
from lib.pyqt_lib.create_thread import create_thread
from lib.pyqt_lib.query_handling import QueryHandling
from lib.pyqt_lib.message_box import message_info_box

class LibraryGame(Game):
    def __init__(self, game_id, game_name, path, cover_img, game_description, sales):
        super().__init__(game_id, game_name, cover_img, game_description)
        self.__path = path
        self.__sales = sales
        self.__rate = ""
        self.__filesize = ""

    def run(self):
        self.add_to_inventory()
        self.download()
        return 0

    def add_to_inventory(self):

        try:
            self.worker = QueryHandling(game_id=self.game_id)

            self.thread = create_thread(self.worker, self.worker.add_to_inventory_query)
            self.thread.start()

            self.thread.finished.connect(lambda: message_info_box(self, "The game has been successfully added to the inventory!"))

        except AssertionError as e:
            message_info_box(self, e)

        return 0

    def download(self):
        return 0

    def rate(self):
        return 0

    def __str__(self):
        return ""
