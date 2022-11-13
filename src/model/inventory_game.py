from src.model.game import Game


class InventoryGame(Game):
    def __init__(self, game, parent_id, local_path=''):
        super().__init__(game.return_game_id(), game.return_game_name())
        self.__parent_id = parent_id
        self.__local_path = local_path

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
