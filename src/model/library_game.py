from src.model.game import Game


class LibraryGame(Game):
    def __init__(self, game_name, game_id):
        super().__init__(game_name, game_id)
        self.vm_path = ""
        self.rate = ""
        self.filesize = ""

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
