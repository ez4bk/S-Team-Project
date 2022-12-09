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

    def test_download(self):
        fami_parent = FamiParent()
        store_game = StoreGame(6, "Snake", "/home/famiowl_files/game_icons/icon_gameid=6.png",
                               "/home/famiowl_files/snake.py", "Eat and grow your snake!", 8)
        fami_parent.get_parent_info_query('test5@test.com', 'test')
        try:
            store_game.download()
        except:
            assert False, "download failed"

    def test_add_like(self):
        fami_parent = FamiParent()
        store_game = StoreGame(6, "Snake", "/home/famiowl_files/game_icons/icon_gameid=6.png",
                               "/home/famiowl_files/snake.py", "Eat and grow your snake!", 8)
        fami_parent.get_parent_info_query('test5@test.com', 'test')
        correct_res = store_game.return_like_count()
        correct_res += 1
        try:
            store_game.add_like()
        except:
            assert False, "add like failed"
        res = store_game.return_like_count()
        assert res == correct_res, "add like failed, value incorrect"

    def test_remove_like(self):
        fami_parent = FamiParent()
        store_game = StoreGame(6, "Snake", "/home/famiowl_files/game_icons/icon_gameid=6.png",
                               "/home/famiowl_files/snake.py", "Eat and grow your snake!", 8)
        fami_parent.get_parent_info_query('test5@test.com', 'test')
        correct_res = store_game.return_like_count()
        correct_res -= 1
        try:
            store_game.remove_like()
        except:
            assert False, "remove like failed"
        res = store_game.return_like_count()
        assert res == correct_res, "remove like failed, value incorrect"