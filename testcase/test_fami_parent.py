import datetime

from lib.base_lib.sql.sql_utils import SqlUtils
from lib.business_lib.game_query import get_top_game_query
from src.model.fami_kid import FamiKid
from src.model.fami_parent import FamiParent
from src.model.inventory_game import InventoryGame
from src.model.store_game import StoreGame

sql_utils = SqlUtils()


class TestFamiParent(object):
    def test_t13_get_kids(self):
        fami_parent = FamiParent()
        res = fami_parent.get_parent_info_query('test5@test.com', 'test')
        assert isinstance(res, FamiParent), 'Creating FamiParent Failed'
        res = fami_parent.get_kids_info_query()
        assert isinstance(res, FamiParent), 'Getting FamiKids Failed'
        for kid in fami_parent.return_kids():
            assert isinstance(kid, FamiKid), 'Creating FamiKids Failed'

    def test_t05_kids_profile(self):
        fami_parent = FamiParent()
        res = fami_parent.get_parent_info_query('test5@test.com', 'test')
        assert isinstance(res, FamiParent), 'Creating FamiParent Failed'
        res = fami_parent.get_kids_info_query()
        assert isinstance(res, FamiParent), 'Getting FamiKids Failed'
        for kid in fami_parent.return_kids():
            assert isinstance(kid.return_profile(), str), 'Getting Profile Failed'

    def test_t08_get_inventory(self):
        fami_parent = FamiParent()
        res = fami_parent.get_parent_info_query('test5@test.com', 'test')
        assert isinstance(res, FamiParent), 'Creating FamiParent Failed'
        res = fami_parent.get_kids_info_query()
        assert isinstance(res, FamiParent), 'Getting FamiKids Failed'

        id_res = fami_parent.get_inventory_query()
        assert isinstance(id_res, list), 'Getting Inventory Failed'

        top_games = get_top_game_query()
        for game in top_games:
            if int(game.return_game_id()) in id_res:
                game.run_game(fami_parent)

        for game in fami_parent.return_inventory():
            assert isinstance(game, InventoryGame), 'Creating Inventory Failed'
            assert not isinstance(game, StoreGame), 'Game Does Not Belong to Inventory'

    def test_sync_database(self):
        fami_parent = FamiParent()
        res = fami_parent.get_parent_info_query('test5@test.com', 'test')
        assert isinstance(res, FamiParent), 'Creating FamiParent Failed'
        res = fami_parent.get_kids_info_query()
        assert isinstance(res, FamiParent), 'Getting FamiKids Failed'

        store_game = StoreGame('99', 'test_sync_database', 'path/to/cover', 'path/to/vm',
                               'test_sync_database_description', '8')
        inventory_game = InventoryGame(store_game, fami_parent, 'path/to/inventory')
        fami_parent.add_to_inventory(inventory_game)
        try:
            fami_parent.sync_database()
        except:
            assert False, 'Inventory Sync Failed'

        res = None
        sql_cmd = 'SELECT * FROM game_inventory WHERE parent_id = "%s" AND game_id = "%s"' % (
            fami_parent.return_parent_id(), inventory_game.return_game_id())
        res = sql_utils.sql_exec(sql_cmd)
        assert res is not None, 'Inventory Not Synced'
        assert res != [], 'Inventory Not Synced'

        fami_kid = FamiKid('99', 'test_sync_database', fami_parent, 'profile', 111, datetime.date.today(), 0)
        fami_parent.add_kid(fami_kid)

        assert fami_kid in fami_parent.return_kids(), 'Kid Not Added'
        try:
            fami_parent.sync_database()
        except:
            assert False, 'Kid Sync Failed'

        res = None
        sql_cmd = 'SELECT * FROM kids WHERE kids_name = "%s" AND parent_id = "%s"' % (
            fami_kid.return_kid_name(), fami_kid.return_parent_id())
        res = sql_utils.sql_exec(sql_cmd)
        assert res is not None, 'Kids Not Synced'
        assert res != [], 'Kids Not Synced'

        sql_cmd = 'DELETE FROM kids WHERE kids_name = "%s" AND parent_id = "%s"' % (
            fami_kid.return_kid_name(), fami_kid.return_parent_id())
        sql_utils.sql_exec(sql_cmd, 0)

        sql_cmd = 'DELETE FROM game_inventory WHERE parent_id = "%s" AND game_id = %s' % (
            fami_parent.return_parent_id(), int(inventory_game.return_game_id()))
        sql_utils.sql_exec(sql_cmd, 0)
