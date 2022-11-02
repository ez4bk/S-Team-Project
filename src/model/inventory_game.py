from src.model.game import Game


class InventoryGame(Game):
    def __init__(self, game_name, game_id):
        super().__init__(game_name, game_id)
        self.local_path = ""
        self.time_limit = ""
        self.time_record = ""

    def run(self):
        return 0

    def stop(self):
        return 0

    def monitor(self):
        return 0

    def delete(self):
        return 0

    def __str__(self):
        return ""
