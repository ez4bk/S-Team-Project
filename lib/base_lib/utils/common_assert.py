# coding=utf-8
import os
import sys

from lib.base_lib.mylog.mylog import _commonlib_log, _commonlib_log_e


def __get_test_case_name():
    f = sys._getframe().f_back
    msg = ""
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if str(filename).lower() == str(__file__).lower():
            f = f.f_back
            continue
        if not str(co.co_name).lower().startswith("test") and not str(co.co_name).lower().endswith("test"):
            f = f.f_back
            continue
        msg = str(co.co_name)
        break
    return msg


def common_assert(flag, desc=""):
    common_assert_equal(flag, desc)


# def common_assert(exp, act, desc):
#     case_name = __get_test_case_name()
#     flag = False
#     try:
#         assert exp == act, desc
#         flag = True
#     except Exception as e:
#         flag = False
#         raise e
#     finally:
#         if flag:
#             _commonlib_log(case_name + ": " + desc + " assert true")
#         else:
#             _commonlib_log_e(case_name + ": " + desc + " assert false")


def common_assert_equal(flag, desc):
    case_name = __get_test_case_name()
    if flag:
        _commonlib_log(case_name + ": " + desc + " assert true")
        assert True, desc
    else:
        _commonlib_log_e(case_name + ": " + desc + " assert false.")
        assert False, str(desc)


if __name__ == '__main__':
    common_assert(True, False, "aaaaaa")
