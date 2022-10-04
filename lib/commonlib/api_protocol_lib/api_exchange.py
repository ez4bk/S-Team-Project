# coding=utf-8
import requests

from commonlib.api_protocol_lib.http_interface import HttpInterface

from commonlib.api_protocol_lib.shell_interface import ShellInterface
# from commonlib.api_protocol_lib.socket_interface import SocketInterface, tcp_call
# from commonlib.api_protocol_lib.thritf_interface import ThriftInterface, thrift_call
# from commonlib.api_protocol_lib.websocket_interface import WebSocketInterface
from commonlib.base_lib.mylog.mylog import log

requests.packages.urllib3.disable_warnings()


def api_exchange(protocol, url, param, method=None, **kwargs):
    """
    request_protocol: http,https,tcp,php,websocket,vm_message
    request_type:   http、https,php支持类型有：get,post,put,delete; vm_message默认为tcp
    port:   请求端口，此端口可以做为tcp、thrift、http等使用
    thrift_source


    :param method:  请求方法
    :param protocol: 协议
    :param param: 参数
    :param url: url或ip
    :param kwargs:
    :return:
    """
    obj = None
    if str(protocol).lower() in ['https', 'http']:
        obj = HttpInterface()
    elif str(protocol).lower() == "websocket":
        from commonlib.api_protocol_lib.websocket_interface import WebSocketInterface
        obj = WebSocketInterface()
    elif str(protocol).lower() == "shell":
        obj = ShellInterface()
    elif str(protocol).lower() == "thrift":
        from commonlib.api_protocol_lib.thritf_interface import ThriftInterface
        obj = ThriftInterface()
    elif str(protocol).lower() == "socket":
        from commonlib.api_protocol_lib.socket_interface import SocketInterface
        obj = SocketInterface()
    if obj is None:
        log("protocol not support")
    result = obj.exchange(url, param, method, **kwargs)
    return result


def api_exchange_http(url, param, method, **kwargs):
    """
     支持http 、https 、 restful 、 sunny 协议
    :param method:  请求方法
    :param param: 参数
    :param url: url或ip
    :param kwargs:
    :return:
    """
    obj = HttpInterface()
    result = obj.exchange(url, param, method, **kwargs)
    return result


def api_exchange_websocket(ip, msg, timeout=10 * 1000, **kwargs):
    """
     支持websocket 协议
    :param ip:  终端ip
    :param msg: 发送请求信息信息
    :param timeout: websocket 连接超时时间
    :param kwargs:
    :return:
    """
    from commonlib.api_protocol_lib.websocket_interface import WebSocketInterface
    obj = WebSocketInterface()
    result = obj.exchange(ip, msg, timeout, **kwargs)
    return result


def api_exchange_shell(server_ip, cmd, timeout=10 * 1000, **kwargs):
    """
     执行shell 指令
    :param server_ip:  服务器ip
    :param cmd: 参数
    :param timeout: 超时设置
    :param kwargs:
    :return:
    """
    obj = ShellInterface()
    result = obj.exchange(server_ip, cmd, timeout, **kwargs)
    return result


def api_exchange_thrift(server_ip, thrift_port, method_name, *args):
    """
     支持thrift 接口
    :param server_ip:  请求方法
    :param thrift_port: 参数
    :param method_name: url或ip
    :param args:
    :return:
    """
    from commonlib.api_protocol_lib.thritf_interface import thrift_call
    result = thrift_call(server_ip, thrift_port, method_name, *args)
    return result


def api_exchange_socket(ip, port, message, timeout=35, **kwargs):
    """
     支持socket协议
    :param ip:  服务器ip
    :param port: 端口
    :param message: 消息
    :param timeout: 超时
    :param kwargs:
    :return:
    """
    from commonlib.api_protocol_lib.socket_interface import tcp_call
    result = tcp_call(ip, port, message, timeout)
    return result


def api_exchange_rpc(ip, method, port, content, namespace, timeout=35, **kwargs):
    """
     支持socket协议
    :param ip:  服务器ip
    :param port: 端口
    :param method: 消息
    :param timeout: 超时
    :param content:
    :param namespace:
    :param kwargs:
    :return:
    """
    from commonlib.api_protocol_lib.rpc_interface import RpcInterface
    rpc = RpcInterface()
    result = rpc.exchange(ip=ip, method=method, content=content, namespace=namespace, port=port, timeout=timeout,
                          **kwargs)
    return result


def api_exchange_restful(url, method, content, timeout=35, **kwargs):
    """
     支持restful协议
    :param url:  url地址
    :param method: url请求方法
    :param timeout: 超时
    :param content:
    :param kwargs:
    :return:
    """
    from commonlib.api_protocol_lib.rpc_interface import RestfulInterface
    res = RestfulInterface()
    result = res.exchange(url=url, method=method, content=content, timeout=timeout, **kwargs)
    return result


# 将class转dict,以_开头的属性不要
def props(obj):
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not callable(value) and not name.startswith('_'):
            pr[name] = value
    return pr


# 将class转dict,以_开头的也要
def props_with_(obj):
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not callable(value):
            pr[name] = value
    return pr


# dict转obj，先初始化一个obj
def dict2obj(obj, dict):
    obj.__dict__.update(dict)
    return obj


class Debug(object):
    def __init__(self):
        self.a = ""
        self.b = ""
        self.c = ""


if __name__ == '__main__':
    aa = {"a": 1, "b": "c"}
    a = Debug()
    del a.b
    # print(dict2obj(a,aa).c)
    print(props(a))
