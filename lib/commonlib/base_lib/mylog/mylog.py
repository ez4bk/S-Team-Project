import datetime
import logging
import os
import sys

from lib.commonlib.base_lib.utils.processpath import cur_file_dir

# sys.stderr = sys.stdout

commonlib_logger = None
user_logger = None
commonlib_fh = None
fh = None
default_log_path = ""
commonlib_log_file_name = ""
log_file_name = ""
formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)

__commonlib_log_flag = True


def __clear_log_handler():
    global commonlib_logger
    # global user_logger
    global commonlib_fh
    global fh
    commonlib_logger.removeHandler(commonlib_fh)
    commonlib_logger.removeHandler(ch)
    user_logger.removeHandler(fh)
    user_logger.removeHandler(commonlib_fh)
    user_logger.removeHandler(ch)


def __add_log_handler():
    global commonlib_logger
    global user_logger
    global commonlib_fh
    global fh
    commonlib_logger.addHandler(commonlib_fh)
    user_logger.addHandler(fh)
    # commonlib_logger.addHandler(commonlib_ch)
    user_logger.addHandler(ch)

    user_logger.addHandler(commonlib_fh)
    if __commonlib_log_flag:
        commonlib_logger.addHandler(ch)


def __init_file_handler(file_path, log_name):
    global formatter
    global commonlib_fh
    global fh
    global commonlib_file_name
    global log_file_name
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    if log_name != "":
        log_file_name = os.path.join(file_path, log_name)
    else:
        log_file_name = os.path.join(file_path, str(datetime.datetime.now().strftime("%Y-%m-%d")) + ".log")
    commonlib_file_name = os.path.join(file_path, "commonlib_" +
                                       str(datetime.datetime.now().strftime("%Y-%m-%d")) + ".log")

    fh = logging.FileHandler(log_file_name, encoding="UTF-8")
    fh.setFormatter(formatter)
    commonlib_fh = logging.FileHandler(commonlib_file_name, encoding="UTF-8")
    commonlib_fh.setFormatter(formatter)


def __init_logger(test_log_path="", log_name=""):
    global commonlib_logger
    global user_logger
    global default_log_path
    global __commonlib_log_flag
    if str(cur_file_dir()).__contains__("commonlib"):
        __commonlib_log_flag = True
    if test_log_path == "":
        path = str(cur_file_dir())
        test_log_path = os.path.join(path, 'log')
    default_log_path = test_log_path
    commonlib_logger = logging.getLogger("commonlib")

    user_logger = logging.getLogger("user")
    commonlib_logger.setLevel(logging.DEBUG)
    user_logger.setLevel(logging.INFO)
    __clear_log_handler()
    __init_file_handler(test_log_path, log_name)
    __add_log_handler()


#
def set_log_path(log_path, log_name):
    """
    设置日志保存路径，此接口为文件保存路径，并非日志文件名，文件名依然使用时间格式进行创建

    :param log_path: log路径。如 D:\debug_log
    """
    __init_logger(log_path, log_name)


def get_log_path():
    """
    获取当前日志保存的路径

    :return: 返回日志保存的路径文件夹
    """
    global default_log_path
    return default_log_path


def get_common_lib_log_file_name():
    global commonlib_log_file_name
    return commonlib_log_file_name


def get_log_file_name():
    global log_file_name
    return log_file_name


def open_commonlib_log(open_flag=True):
    """
    开启公共库日志，调用此接口，公共库部份的日志将也输出到控制台

    :param open_flag: True时开启公共库日志，False时关闭公共库日志，默认为开启
    """
    global __commonlib_log_flag
    __commonlib_log_flag = open_flag
    __init_logger()


def set_log_level(log_level):
    """
    设置日志等级，日志级别从低到高为notset、debug、 info、 warning、 error、 critical，默认为info。设置高级别时，低级别日志将不再打印

    :param log_level:notset、debug、 info、 warning、 error、 critical之一
    """
    if str(log_level).lower() == "notset":
        level = logging.NOTSET
    elif str(log_level).lower() == "debug":
        level = logging.DEBUG
    elif str(log_level).lower() == "info":
        level = logging.INFO
    elif str(log_level).lower() == "warning":
        level = logging.WARNING
    elif str(log_level).lower() == "error":
        level = logging.ERROR
    elif str(log_level).lower() == "critical":
        level = logging.CRITICAL
    else:
        level = logging.INFO
    global user_logger
    global commonlib_logger
    print("set mylog level " + str(level))
    user_logger.setLevel(level)
    commonlib_logger.setLevel(level)


def log_d(msg):
    """
    调试级别日志打印

    :param msg:  要打印的日志信息
    """
    auxiliary_msg = __get_auxiliary_info()
    user_logger.debug(auxiliary_msg + str(msg))
    # commonlib_logger.debug(auxiliary_msg + str(msg))


def log_i(msg):
    """
    信息级别日志打印

    :param msg:  要打印的日志信息
    """
    auxiliary_msg = __get_auxiliary_info()
    user_logger.info(auxiliary_msg + str(msg))
    # commonlib_logger.info(auxiliary_msg + str(msg))


def log_w(msg):
    """
    告警级别日志打印

    :param msg:  要打印的日志信息
    """
    auxiliary_msg = __get_auxiliary_info()
    user_logger.warning(auxiliary_msg + str(msg))
    # commonlib_logger.warning(auxiliary_msg + str(msg))


def log_e(msg):
    """
    错误级别日志打印

    :param msg:  要打印的日志信息
    """
    auxiliary_msg = __get_auxiliary_info()
    user_logger.error(auxiliary_msg + str(msg))
    # commonlib_logger.error(auxiliary_msg + str(msg))


def log(msg):
    """
    信息级别日志打印

    :param msg:  要打印的日志信息
    """
    log_i(msg)


def _commonlib_log_d(msg):
    """
    调试级别日志打印

    :param msg:  要打印的日志信息
    """
    auxiliary_msg = __get_auxiliary_info()
    commonlib_logger.debug(auxiliary_msg + str(msg))


def _commonlib_log_i(msg):
    """
    信息级别日志打印

    :param msg:  要打印的日志信息
    """
    auxiliary_msg = __get_auxiliary_info()
    commonlib_logger.info(auxiliary_msg + str(msg))


def _commonlib_log_w(msg):
    """
    告警级别日志打印

    :param msg:  要打印的日志信息
    """
    auxiliary_msg = __get_auxiliary_info()
    commonlib_logger.warning(auxiliary_msg + str(msg))


def _commonlib_log_e(msg):
    """
    错误级别日志打印

    :param msg:  要打印的日志信息
    """
    auxiliary_msg = __get_auxiliary_info()
    commonlib_logger.error(auxiliary_msg + str(msg))


def _commonlib_log(msg):
    """
    信息级别日志打印

    :param msg:  要打印的日志信息
    """
    _commonlib_log_i(msg)


def __get_auxiliary_info():
    f = sys._getframe().f_back
    msg = ""
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if str(filename).lower() == str(__file__).lower():
            f = f.f_back
            continue
        msg = "[" + str(os.path.basename(co.co_filename)) + "->" + str(co.co_name) + "->" + str(f.f_lineno) + "]-"
        break
    return msg


__init_logger()

if __name__ == '__main__':
    # set_log_level("error")
    log_i("77777")
    open_commonlib_log(True)
    _commonlib_log("111")
    # _commonlib_log("222")
    # _commonlib_log("333")
    # # set_log_level("warning")
    # log_w("5555")
    # _commonlib_log_e("66666")

    # set_log_path("D:")
    # log_d("888")
    # _commonlib_log_e("99999")
    # log_w("000000")
    #
    # log_w("5555")
    # set_log_path(os.path.dirname("D:\\"), "build.log")
    # _commonlib_log_e("66666")
    # log_i("77777")
