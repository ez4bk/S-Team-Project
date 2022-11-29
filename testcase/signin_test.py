import pytest

from src.control.signin_control import SigninWindow

signin_window = SigninWindow()


class SigninTest(object):

    @pytest.mark.monitor_skip_test
    def test_signin_t04(self):
        userid = 'test3@test.com'
        pwd = 'test'
        signin_window = SigninWindow(None, userid, pwd)
        if signin_window.signin_query(userid, pwd) is str:
            assert False, "Error"
