from src.model.store_game import StoreGame
from src.model.fami_parent import FamiParent
from config.project_info import DOWNLOAD_DIR



class TestStoreGame(object):

    def test_add_to_inventory(self):
        fami_parent = FamiParent()
        store_game = StoreGame(6, "Snake", "/home/famiowl_files/game_icons/icon_gameid=6.png",
                               "/home/famiowl_files/snake.py", "Eat and grow your snake!", 8)
        fami_parent.get_parent_info_query('test5@test.com', 'test')
        try:
            store_game.add_to_inventory(fami_parent, DOWNLOAD_DIR)
        except:
            assert False, "add to inventory failed"
