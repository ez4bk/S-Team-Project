from src.model.game import Game


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
        return 0

    def download(self):
        return 0

    def rate(self):
        return 0

    def __str__(self):
        return ""
