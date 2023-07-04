class Game:
    def __init__(self, game_id, game_name, cover_img, game_description):
        self.__game_id = game_id
        self.__game_name = game_name
        self.__cover_img = cover_img
        self.__game_description = game_description

    def run_game(self, fami_parent):
        pass

    def download(self):
        pass

    def return_game_id(self):
        return str(self.__game_id)

    def return_game_name(self):
        return str(self.__game_name)

    def return_cover_img(self):
        return str(self.__cover_img)

    def return_game_descr(self):
        return str(self.__game_description)
