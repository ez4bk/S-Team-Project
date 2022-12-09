from datetime import date

from lib.base_lib.sql.sql_utils import SqlUtils
from src.model.fami_parent import FamiParent

sql_utils = SqlUtils()


class TestFamiKid(object):
    def test_init_playtime(self):
        fami_parent = FamiParent()
        res = fami_parent.get_parent_info_query('test5@test.com', 'test')
        assert isinstance(res, FamiParent), 'Creating FamiParent Failed'
        res = fami_parent.get_kids_info_query()
        assert isinstance(res, FamiParent), 'Getting FamiKids Failed'
        for kid in fami_parent.return_kids():
            try:
                kid.init_playtime()
            except:
                assert False, 'Init Playtime Failed'
            sql_cmd = 'SELECT last_played FROM kids WHERE id = %s' % kid.return_kid_id()
            res = sql_utils.sql_exec(sql_cmd)
            assert res != [], 'Init Playtime Failed'
            assert res[0][0] == date.today(), 'Playtime Not Up-to-date'

    def test_sync_database(self):
        fami_parent = FamiParent()
        res = fami_parent.get_parent_info_query('test5@test.com', 'test')
        assert isinstance(res, FamiParent), 'Creating FamiParent Failed'
        res = fami_parent.get_kids_info_query()
        assert isinstance(res, FamiParent), 'Getting FamiKids Failed'

        for kid in fami_parent.return_kids():
            kid.set_time_remaining(0)
            kid.sync_database()
            sql_cmd = 'SELECT time_played_today FROM kids WHERE id = %s' % kid.return_kid_id()
            res = sql_utils.sql_exec(sql_cmd)
            assert res != [], 'Init Playtime Failed'
            assert res[0][0] == round(kid.return_time_limit() / 60), 'Playtime Not Up-to-date'
            kid.set_time_remaining(kid.return_time_limit())
            kid.sync_database()
