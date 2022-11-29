from config.sql_query.account_query import parent_id_check, parent_signin
from lib.base_lib.sql.sql_utils import SqlUtils
from lib.base_lib.utils.aes_pass import AESCipher
from src.control.signin_control import SigninWindow

signin_window = SigninWindow()
aes_cipher = AESCipher()


def verify_pwd(user_input, pwd):
    try:
        if aes_cipher.decrypt_main(pwd) == user_input:
            return True
        else:
            return False
    except Exception as e:
        assert False, e


class SigninTest(object):

    def test_signin_t04(self):
        userid = 'test3@test.com'
        pwd = 'test'
        sql_utils = SqlUtils()
        try:
            res = sql_utils.sql_exec(parent_id_check.format(userid), 1)[0][0]
        except Exception as e:
            assert False, 'Fetch parent info failed!'

        if res is None:
            assert False, "Fetch parent info failed!"
        elif res == 0:
            assert False, "User does not exist"

        try:
            res = sql_utils.sql_exec(parent_signin.format(userid), 1)[0]
        except Exception as e:
            assert False, 'Fetch parent info failed!'

        if not verify_pwd(pwd, res[1]):
            assert False, "Password Incorrect!"
        else:
            pass
