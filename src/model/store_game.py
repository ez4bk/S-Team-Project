from src.model.game import Game


class StoreGame(Game):
    def __init__(self, game_id, game_name, cover_img, path, game_description, sales):
        super().__init__(game_id, game_name, cover_img, game_description)
        self.__path = path
        self.__sales = sales
        self.__rate = ""
        self.__filesize = ""

    def run(self):
        self.add_to_inventory()
        self.download()
        return 0

    def add_to_inventory(self, fami_parent):
        inventory = fami_parent.return_inventory()
        for game in inventory:
            if game.return_game_id() == self.return_game_id():
                return "Game already in inventory"
            else:
                fami_parent.add_to_inventory(self)
        return fami_parent

    def download(self):
        return 0

    def rate(self):
        return 0

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
    a = StoreGame('1', 'abc', 'img', 'path', 'des', 'sales')
    print(a.return_game_id())
