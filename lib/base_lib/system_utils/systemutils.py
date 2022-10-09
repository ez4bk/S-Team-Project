# coding=utf-8

import datetime
import re

import psutil as psutil

from lib.base_lib.mylog.mylog import _commonlib_log, log


def get_current_time(new_format="%Y-%m-%d %H:%M:%S.%f"):
    """
    获取当前时间,返回按format格式输出，如：  2020-04-02 15:58:08.905

    :param new_format: 显示的格式，默认："%Y-%m-%d %H:%M:%S".%f

    :return: 返回当前时间
    """
    if new_format == "%Y-%m-%d %H:%M:%S.%f":
        return datetime.datetime.now().strftime(new_format)[:-3]
    else:
        return datetime.datetime.now().strftime(new_format)


# # 获取脚本文件的当前路径
# def cur_file_dir():
#     """
#     获取当前文件路径,如果是编译后，则返回编译后的文件路径，
#
#     :return:
#     """
#     # 获取脚本路径
#     path = sys.path[0]
#     # 判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
#     if os.path.isdir(path):
#         return path
#     elif os.path.isfile(path):
#         return os.path.dirname(path)


# 打印结果

def get_pid_list():
    """
    获取进程的pid列表。

    :return: 返回指定进程名的pid列表
    """
    process_list = list(psutil.process_iter())  # 获取所有的进行信息
    regex = "pid=(\d+),\sname=\'(.+?)\'"  # 正则获取进程信息
    pid_list = []
    for line in process_list:
        process_info = str(line)
        ini_regex = re.compile(regex)
        result = ini_regex.search(process_info)
        if result is not None:  # 添加指定进程名的pid到列表中
            pid_list.append((result.group(2), result.group(1)))
            # pid_list.append(str(result.group(1)))
    return pid_list


def get_pid(process_name):
    """
    获取进程的pid列表。

    :return: 返回指定进程名的pid列表
    """
    pid_list = get_pid_list()
    _commonlib_log(pid_list)
    for a in pid_list:
        if a[0] == process_name:
            _commonlib_log("get " + process_name + " pid " + str(a[1]))
            return str(a[1])
    return ""


def get_system_platform():
    import platform
    tmp = platform.system()
    log("current platform is " + str(tmp))
    return str(tmp)


if __name__ == '__main__':
    _commonlib_log(get_pid_list())
