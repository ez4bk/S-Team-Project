# coding=utf-8
from commonlib.base_lib.network import thrift_utils

thrift_server_ip = ""
thrift_source = ""


def thrift_call(server_ip, thrift_port, method_name, *args):
    return thrift_utils.call_remote(method_name, thrift_source, server_ip, thrift_port, timeout=60 * 1000, *args)


class ThriftInterface(object):

    @staticmethod
    def exchange(server_ip, param, method_name, **kwargs):
        port = kwargs["port"]
        return thrift_call(server_ip, port, method_name, param)

