# coding=utf-8
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport, TSocket


def call_remote(func, module, server_ip=None, port=9091, timeout=None, *args):
    transport = None
    try:

        socket = TSocket.TSocket(server_ip, port)
        """设置超时时间60s"""

        socket.setTimeout(60 * 1000)
        if timeout:
            socket.setTimeout(timeout * 1000)

        transport = TTransport.TBufferedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        imp = __import__(module, fromlist=True)
        tc = getattr(imp, 'Client', None)
        client = tc(protocol)
        transport.open()
        if len(args) == 0:
            ret = eval("client.%s" % (func))()
        else:
            ret = eval("client.%s" % (func))(*args)
    except Exception:
        if transport:
            transport.close()
        raise
    # finally:
    if transport:
        transport.close()

    return ret
