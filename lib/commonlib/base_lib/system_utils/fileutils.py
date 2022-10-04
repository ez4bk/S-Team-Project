# coding=utf-8
import json
import os
import re
import shutil
import time

import simplejson

from lib.commonlib.base_lib.mylog.mylog import _commonlib_log
from lib.commonlib.base_lib.system_utils.myos import MyOs


def write(file_name, msg, append=True):
    """
    文件写操作，如果文件不存在，将创建文件。根据append决定文件重新写入还是文件从最后添加写入

    :param append:  当为True时，追加写入；当为False时，文件从头写入
    :param file_name:   要写入的文件名称，文件名不存在则重新创建，但无法创建文件夹，因此必须保证文件所在的文件夹存在
    :param msg: 要写入到文件中的内容，类型为str
    """
    if append:
        f = open(file_name, "a+", encoding='utf-8')
    else:
        f = open(file_name, "w", encoding='utf-8')
    f.write(msg)
    f.close()


def create_dir(path):
    """
    创建文件夹，支持同时创建多个层级，如 D:\\aaa\\bbb\\ccc

    :param path: 要创建的文件夹名称
    """
    result = os.path.exists(path)
    if not result:
        os.makedirs(path)


def del_dir(path):
    """
    删除文件夹，并且删除文件夹下的所有文件与文件夹

    :param path:    要删除的文件夹名称
    """
    shutil.rmtree(path)


def create_file(path):
    """
    创建文件，如果文件所在的文件夹不存在，将同时被创建

    :param path:    要创建的文件名称
    """
    if not os.path.exists(os.path.dirname(path)) and os.path.dirname(path) != "":
        create_dir(os.path.dirname(path))
    write(path, "", False)


def del_file(file_name):
    """
    删除文件，文件不存在时，不进行操作

    :param file_name:   要删除的文件
    """
    if os.path.exists(file_name):
        os.unlink(file_name)


def list_dir(path):
    """
    列出所有的文件与文件夹,文件夹在内部的不再进行列出

    :param path:    文件夹路径名称

    :return:    返回文件夹下所有的文件与文件夹名称，类型为list，如： ['auto_run.bat', 'chromedriver.exe', 'command_process.py', 'Cweb']
    """
    return os.listdir(path)


def get_file_md5(file_path):
    """
    获取本地文件md5值

    :param file_path: 文件路径

    :return: md5值
    """
    my_os = MyOs()
    if not os.path.isfile(file_path):
        _commonlib_log("the path is not a file")
        return ""
    cmd = "certutil -hashfile \"" + file_path + "\" MD5"
    _commonlib_log(cmd)
    result = my_os.process(cmd)
    for a in result:
        if a == result[0]:
            continue
        msg = a.decode(encoding="GBK")
        msg = re.findall("(.*)\r", msg)[0]
        print(msg)
        msg = str(msg).replace(" ", "")
        if len(msg) == 32:
            return msg
    return ""


def get_file_size(file_name):
    """
    获取文件大小

    :param file_name:   文件名称

    :return:    返回文件的大小，类型为int
    """
    return os.path.getsize(file_name)


def _fileTime(file):
    _commonlib_log(os.path.getatime(file))
    return [
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getatime(file))),  # 输出文件访问时间
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(file))),  # 输出文件最近修改时间
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(file)))  # 输出文件的创建时间
    ]


def load_config_file(file_name, coding="utf-8"):
    if not os.path.exists(file_name):
        config = {}
    else:
        json_file = open(file_name, 'r', encoding=coding)
        config = simplejson.load(json_file)
        json_file.close()
    return config


def save_config_file(file_name, json_buf, coding="utf-8"):
    if not os.path.exists(file_name):
        create_file(file_name)
    json_file = open(file_name, 'w+', encoding=coding)
    json_file.write(json.dumps(json_buf))
    json_file.close()


if __name__ == "__main__":
    print(get_file_size("D:\\ftp\\command_process.py"))
