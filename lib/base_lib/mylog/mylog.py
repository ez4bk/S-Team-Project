import datetime
import logging
import os
import sys

from config.project_info import LOG_DIR

# sys.stderr = sys.stdout
user_logger = None
fh = None
default_log_path = LOG_DIR
log_file_name = ""
formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)


def __clear_log_handler():
    """
    Clear log handler
    :return:
    """
    global fh
    user_logger.removeHandler(fh)
    user_logger.removeHandler(ch)


def __add_log_handler():
    """
    Add log handler
    :return:
    """
    global user_logger
    global fh
    user_logger.addHandler(fh)
    user_logger.addHandler(ch)


def __init_file_handler(file_path, log_name):
    """
    Initialise log file handler
    :param file_path: path to log file
    :param log_name: log name
    :return:
    """
    global formatter
    global fh
    global log_file_name
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    if log_name != "":
        log_file_name = os.path.join(file_path, log_name)
    else:
        log_file_name = os.path.join(file_path, str(datetime.datetime.now().strftime("%Y-%m-%d")) + ".log")

    fh = logging.FileHandler(log_file_name, encoding="UTF-8")
    fh.setFormatter(formatter)


def __init_logger(test_log_path="", log_name=""):
    global user_logger
    global default_log_path
    if test_log_path == "":
        test_log_path = LOG_DIR
    default_log_path = test_log_path

    user_logger = logging.getLogger("user")
    user_logger.setLevel(logging.DEBUG)
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
    # global commonlib_log_file_name
    # return commonlib_log_file_name
    global log_file_name
    return log_file_name


def get_log_file_name():
    global log_file_name
    return log_file_name


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
    # print("set mylog level " + str(level))
    user_logger.setLevel(level)


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
    log_d(msg)


def _commonlib_log_i(msg):
    """
    信息级别日志打印

    :param msg:  要打印的日志信息
    """
    log_i(msg)


def _commonlib_log_w(msg):
    """
    告警级别日志打印

    :param msg:  要打印的日志信息
    """
    log_w(msg)


def _commonlib_log_e(msg):
    """
    错误级别日志打印

    :param msg:  要打印的日志信息
    """
    log_e(msg)


def _commonlib_log(msg):
    """
    信息级别日志打印

    :param msg:  要打印的日志信息
    """
    log_i(msg)


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
    pass
