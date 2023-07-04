from config.project_info import DOWNLOAD_DIR
from src.model.fami_parent import FamiParent
from src.model.store_game import StoreGame


class TestStoreGame(object):

    def test_run_game(self):
        fami_parent = FamiParent()
        store_game = StoreGame(6, "Snake", "/home/famiowl_files/game_icons/icon_gameid=6.png",
                               "/home/famiowl_files/snake.py", "Eat and grow your snake!", 8)
        fami_parent.get_parent_info_query('test5@test.com', 'test')
        try:
            store_game.run_game(fami_parent)
        except:
            assert False, "run game failed"
        assert fami_parent.return_inventory() != [], "Empty inventory"
        game = fami_parent.return_inventory()[0]
        assert int(game.return_game_id()) == int(store_game.return_game_id()), "Wrong game"

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
        correct_res = int(store_game.return_like_count())
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
        correct_res = int(store_game.return_like_count())
        correct_res -= 1
        try:
            store_game.remove_like()
        except:
            assert False, "remove like failed"
        res = store_game.return_like_count()
        assert res == correct_res, "remove like failed, value incorrect"
