from src.model.game import Game


class InventoryGame(Game):
    def __init__(self, game, fami_parent, local_path=''):
        super().__init__(game.return_game_id(), game.return_game_name())
        self.__fami_parent = fami_parent
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
