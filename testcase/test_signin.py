from src.control.signin_control import SigninWindow

signin_window = SigninWindow()


class TestSignin(object):
    def test_signin_T04(self):
        userid = 'test3@test.com'
        pwd = 'test'
        signin_window = SigninWindow(None, userid, pwd)
        assert signin_window.signin_query(userid, pwd)
