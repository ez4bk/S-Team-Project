class Game:
    def __init__(self, game_id, game_name, cover_img, game_description):
        self.__game_id = game_id
        self.__game_name = game_name
        self.__cover_img = cover_img
        self.__game_description = game_description

    def run(self):
        return 0

    def __str__(self):
        return ""
