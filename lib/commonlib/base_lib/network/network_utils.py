# coding=utf-8
import os
import socket
import sys

from lib.commonlib.base_lib.mylog.mylog import _commonlib_log
from lib.commonlib.base_lib.system_utils.myos import MyOs


def check_ip_reachable(device_ip):
    """
    确认IP是否可被网络访问。使用ping机制，对device_ip进行访问

    :param device_ip: 要确认是否网络可达的IP地址

    :return: 可以访问返回True，其它返回False
    """
    _commonlib_log("check ip reachable " + device_ip)
    cmd = "ping -w 1 -n 1 " + device_ip
    my_os = MyOs()
    result = my_os.process(cmd)
    flag = True
    for a in result:
        b = a.decode("gbk")
        if b.__contains__(u'请求超时') or b.__contains__("100% packet loss"):
            flag = False
            break

    _commonlib_log("check ip reachable return " + str(flag))
    return flag


def get_host_ip():
    """
    获取本地IP地址

    :return:    返回IP地址
    """
    if str(sys.platform).lower().__contains__("linux"):
        return __get_ip()
    else:
        return __windows_get_host_ip()


def __windows_get_host_ip():
    """
    查询本机ip地址
    :return:
    """
    ip = ""
    try:
        print("111111111")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        pass
    finally:
        s.close()

    return ip


def __get_ip():
    # 注意外围使用双引号而非单引号,并且假设默认是第一个网卡,特殊环境请适当修改代码
    out = os.popen(
        "ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -1").read()
    ip = out.split('\n')[0]

    return ip


if __name__ == '__main__':
    check_ip_reachable("172.28.100.112")
