# coding=utf-8
import base64
from functools import wraps

from lib.commonlib.base_lib.mylog.mylog import _commonlib_log, log


def base64encode(source):
    """
    base64数据加密。可使用网址进行校验：http://tool.oschina.net/encrypt?type=3

    :param source:  要进行base64加密的数据
    :return:    返回base64加密后的数据
    """
    debug = base64.b64encode(source.encode('utf-8'))
    return str(debug, encoding="utf-8")


def base64decode(target):
    """
    base64数据解密。可使用网址进行校验：http://tool.oschina.net/encrypt?type=3

    :param target: 要进行base64解密的数据
    :return:    返回解密后的数据
    """
    base64_decrypt = base64.b64decode(target.encode('utf-8'))
    return str(base64_decrypt, 'utf-8')


def func_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log(f">>>>>>>>>>>>>>>>>function start {func.__name__}")
        log(f"func {func.__name__} args " + str(args))
        log(f"func {func.__name__} kwargs " + str(kwargs))
        result = func(*args, **kwargs)
        log(f"func {func.__name__} ret " + str(result))
        log(f"<<<<<<<<<<<<<<<<<function end {func.__name__}")
        return result

    return wrapper


def vm_process(func, exchange_type="vmmsg"):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log(f">>>>>>>>>>>>>>>>>function start {func.__name__}")
        log(f"func {func.__name__} args " + str(args))
        log(f"func {func.__name__} kwargs " + str(kwargs))
        result = func(*args, **kwargs)
        log(f"func {func.__name__} ret " + str(result))
        log(f"<<<<<<<<<<<<<<<<<function end {func.__name__}")
        return result

    return wrapper


# def loop_utils_timeout(func, timeout):
#     begin = time.time()
#     while True:
#         if func():
#             _commonlib_log("exec func success")
#             return True
#         if time.time() - begin > timeout / 1000:
#             _commonlib_log_e("exec func timeout!!!")
#             return False
#         time.sleep(0.3)


def wait_process_success(func, timeout):
    _commonlib_log("111111111111")


if __name__ == '__main__':
    wait_process_success("", "")
