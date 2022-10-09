#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@author: chengll
@contact: chengll@ruijie.com
@software: PyCharm
@time: 2019/12/2 16:16
"""
from lib.base_lib import log
from lib.base_lib.network import tcp_utils


def tcp_call(ip, port, message, timeout=35):
    tmp_sock = tcp_utils.connect(ip, port)
    if tmp_sock is None:
        return False
    else:
        try:
            tmp_sock.send(str.encode(message))
            tmp_data = tcp_utils.receive_protocol_data(tmp_sock, timeout * 1000)
            if type(tmp_data) == bytes:
                tmp_data = bytes.decode(tmp_data)
            return tmp_data
        except Exception as connect_error:
            log(connect_error)


class SocketInterface(object):
    @staticmethod
    def exchange(server_ip, message, timeout=35, **kwargs):
        port = kwargs["port"]
        return tcp_call(server_ip, port, message, timeout)


if __name__ == "__main__":
    SocketInterface.exchange("172.31.204.230", "hello world", 35, port=50007)
