# coding=utf-8
import binascii
import json
import socket
import time
import traceback

from lib.commonlib.base_lib.mylog.mylog import log, _commonlib_log
from lib.commonlib.base_lib.network.network_utils import get_host_ip

STX = 0x01
ETX = 0xFF


def __get_data_length(data):
    """
    获取数据的长度，返回2个字节的16进制数据

    :param data:数据内容

    :return: 2个字节16进制数据
    """
    length = len(data) / 2
    return "{:04x}".format(int(length))
    # print(data)
    # print(len(data))
    # length = len(data) / 2
    # high = length / 0x100
    # low = length % 0x100
    # tmp1 = chr(int(high))
    # tmp2 = chr(int(low))
    # data_length = binascii.hexlify(tmp1.encode()).upper() + binascii.hexlify(tmp2.encode()).upper()
    # print(data_length.decode())
    # return data_length.decode()


def __tran_length_to_int(length_data):
    """
    将2字节的长度转换成Int

    :param length_data:  2字节数据，将转换成int的数据源

    :return: 返回Int数据
    """
    high = int(length_data[:2], 16)
    low = int(length_data[2:], 16)
    length = high * 0x100 + low
    return length


def __package_protocol_data(data):
    """
    将数据按json协议进行打包，并加上2字节的数据长度在包头

    :param data: 要进行打包的数据

    :return: 返回打包后的数据
    """
    data = json.dumps(data)
    buf = ""
    tmp = binascii.b2a_hex(data.encode()).decode()
    # buf += "{:02x}".format(int(STX))
    buf += __get_data_length(tmp)
    buf += tmp
    # buf += "{:02x}".format(int(ETX))
    _commonlib_log(buf)
    return buf


def connect(ip, port, timeout=30):
    """
    TCP连接。connect要与disconnect配对使用

    :param timeout: 连接超时时间
    :param ip: 要连接的IP地址
    :param port: 要连接的端口

    :return: 返回sock
    """
    _commonlib_log((">>>tcp connect " + str(ip) + "#" + str(port)))
    is_connect = True
    sock = None
    for a in range(3):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)  # 设置超时旱为30S
            sock.connect((ip, port))
            break
        except:
            _commonlib_log(traceback.format_exc())
            sock = None
            time.sleep(1)
    if not is_connect:
        log(("connect " + str(ip) + ":" + str(port) + " error"))
    else:
        _commonlib_log(">>>>>>tcp connect " + str(ip) + "#" + str(port) + " success!!!")

    return sock


def send_protocol_data(sock, data):
    """
    发送协议数据，数据会经过协议打包接口进行组包后发送。

    :param sock: sock
    :param data: 要发送的数据，data格式为dict类型，如{"cmd": "create_no_upload_flag"}

    """
    buf = __package_protocol_data(data)
    # _commonlib_log("send buf:" + str(bytearray.fromhex(buf).decode()))
    sock.send(bytearray.fromhex(buf))


def send(sock, data):
    """
    判断数据，不带任何协议，直接由sock进行透传。正常进行TCP通讯，需要增加数据协议，否则在接收方，无法知道发送的数据长度，会带来麻烦

    :param sock: sock
    :param data: 要发送的数据内容

    """
    sock.send(data)


def receive(sock, length):
    """
    按长度进行数据接收。

    :param sock: sock
    :param length: 要接收的数据长度

    :return: 返回接收到的数据报文
    """
    return sock.recv(length)


def receive_protocol_data(sock, timeout):
    """
    超时时间内，接收协议数据

    :param sock: sock
    :param timeout: 超时时间，单位ms

    :return: 返回接收到去除了协议的数据内容，类型为str，需要调用json.loads转换成json
    """
    start = time.time()
    while True:
        data = sock.recv(2)
        _commonlib_log(binascii.b2a_hex(data))
        sock.settimeout(timeout / 1000)
        if data != "":
            data_length = __tran_length_to_int(binascii.b2a_hex(data).decode())
            _commonlib_log("tcp data length:" + str(data_length))
            data = ""
            while True:
                tmp = sock.recv(data_length)
                tmp_length = len(tmp)
                data += binascii.b2a_hex(tmp).decode()
                _commonlib_log("expect receive length " + str(data_length) + " ; act receive length " + str(len(tmp)))
                if tmp_length == data_length:
                    break
                else:
                    data_length = data_length - tmp_length
            break
        elif timeout and (time.time() - start) > timeout / 1000:
            raise Exception("Receive timed out waiting for PIN-Pad response.")
    return bytearray.fromhex(data)


def disconnect(sock):
    """
    断开sock连接

    :param sock: sock
    """
    if sock is not None:
        sock.close()


def create_server(port):
    """
    创建服务端并绑定端口。端口不可同时被多个服务端绑定，同时因1000以前端口很多都被系统占用，不建议进行使用

    :param port: 要绑定的端口
    :return:    返回服务端 server
    """
    ip = get_host_ip()
    # ip = "127.0.0.1"
    log(("create tcp server " + ip + ":" + str(port)))
    ip_port = (ip, port)
    web = socket.socket()
    web.bind(ip_port)
    return web


def create_server_with_ip(ip, port):
    """
    创建服务端并绑定端口。端口不可同时被多个服务端绑定，同时因1000以前端口很多都被系统占用，不建议进行使用

    :param ip:
    :param port: 要绑定的端口
    :return:    返回服务端 server
    """
    # ip = "127.0.0.1"
    log(("create tcp server " + ip + ":" + str(port)))
    ip_port = (ip, port)
    web = socket.socket()
    web.bind(ip_port)
    return web


def listen(server, max_socket):
    """
    服务端监听，服务端开发使用

    :param server:  服务端server
    :param max_socket: 最大支持多少socket链路维持
    """
    server.listen(max_socket)


def accept(server):
    """
    等待服务端被连接，连接后，返回socket。开发TCP服务端需要

    :param server: 服务端SERVER

    :return: 有客户端连接时，返回socket，无连接时，将阻塞直到超时时间到
    """
    conn, address = server.accept()
    return conn


def set_server_timeout(server, timeout):
    """
    设置服务端accept超时时间

    :param timeout:    超时时间,单位为ms
    :param server: 服务端SERVER

    """
    server.settimeout(timeout / 1000)


def close_server(server):
    """
    关闭服务端server，此接口必须与 create_server 配套使用，否则会出现内存溢出

    :param server:  服务端server
    """
    _commonlib_log("close server")
    if server is not None:
        server.close()


if __name__ == '__main__':
    # data = "7b22636d64223a2022636f7079222c2022736f75726365223a20225c5c5c5c3137322e32312e3131322e3133365c5c645c5c5243445c5c5c75366434625c75386264355c75386664305c75383432355c75376563345c5c5c75383165615c75353261385c75353331365c5c5c75376635315c75373664385c75363537305c75363336655c5c446174615c5c3132332e646f63222c2022746172676574223a2022443a5c5c227d"
    # print(data)
    # print(len(data))
    # length = len(data) / 2
    # tmp = "{:04x}".format(int(length))
    # print(tmp)

    # tmp_cmd = {"cmd": "update", "source": r"\\172.21.112.136\d\RCD\测试运营组\自动化\网盘数据\Data\123.txt", "target": "D:\\"}
    tmp_sock = connect("172.20.113.80", 10122)
    # send_protocol_data(tmp_sock, tmp_cmd)
    # tmp_data = receive_protocol_data(tmp_sock, 5 * 1000)
    # _commonlib_log(tmp_data)
# tmp = binascii.b2a_hex(json.dumps({"result": "ok"}).encode())
# print(tmp)
# print(tmp[1])
# print(binascii.a2b_hex(tmp))
# print(bytearray.fromhex("0100107b22726573756c74223a20226f6b227dff"))
# _commonlib_log("send buf:" + binascii.b2a_hex("0100107b22726573756c74223a20226f6b227dff"))
# print(binascii.unhexlify("0100107b22726573756c74223a20226f6b227dff".encode()))
