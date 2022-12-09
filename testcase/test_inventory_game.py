from src.model.inventory_game import InventoryGame
from src.model.store_game import StoreGame
from src.model.fami_parent import FamiParent
from config.sql_query.game_query import get_likes

from lib.base_lib.sql.sql_utils import SqlUtils

sql_utils = SqlUtils()


class TestInventoryGame(object):

    def test_run_game(self):
        return

    def test_stop_game(self):
        return

    def test_get_like_count(self):
        store_game = StoreGame(6, "Snake", "/home/famiowl_files/game_icons/icon_gameid=6.png",
                               "/home/famiowl_files/snake.py", "Eat and grow your snake!", 8)
        fami_parent = FamiParent()
        inventory_game = InventoryGame(store_game, fami_parent)
        assert inventory_game.return_like_count() != 8, "get like count failed"

    def test_hit_like(self):
        store_game = StoreGame(6, "Snake", "/home/famiowl_files/game_icons/icon_gameid=6.png",
                               "/home/famiowl_files/snake.py", "Eat and grow your snake!", 8)
        fami_parent = FamiParent()
        inventory_game = InventoryGame(store_game, fami_parent)
        try:
            inventory_game.hit_like()
        except:
            assert False, 'hit like failed'
        assert inventory_game.return_liked() == True, "Failed, Incorrect result"

    def test_hit_unlike(self):
        store_game = StoreGame(6, "Snake", "/home/famiowl_files/game_icons/icon_gameid=6.png",
                               "/home/famiowl_files/snake.py", "Eat and grow your snake!", 8)
        fami_parent = FamiParent()
        inventory_game = InventoryGame(store_game, fami_parent)
        try:
            inventory_game.hit_unlike()
        except:
            assert False, 'hit unlike failed'
        assert inventory_game.return_liked() == False, "Failed, Incorrect result"

    def test_sync_like(self):
        store_game = StoreGame(6, "Snake", "/home/famiowl_files/game_icons/icon_gameid=6.png",
                               "/home/famiowl_files/snake.py", "Eat and grow your snake!", 8)
        fami_parent = FamiParent()
        inventory_game = InventoryGame(store_game, fami_parent)
        inventory_game.hit_like()
        sql_cmd = "select like_count from game_store where game_id = 6;"
        correct_res = sql_utils.sql_exec(sql_cmd, 1)[0][0]
        correct_res += 1
        try:
            inventory_game.sync_likes()
        except:
            assert False, 'sync like failed'
        res = sql_utils.sql_exec(sql_cmd, 1)[0][0]
        assert res == correct_res, "failed, incorrect like count"

