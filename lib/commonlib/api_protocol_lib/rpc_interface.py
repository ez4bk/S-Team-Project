#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@author: chengll
@contact: chengll@ruijie.com
@software: PyCharm
@time: 2020/3/19 19:07
"""
import json
import os
from emei.framework import client as rccpclient
from commonlib.base_lib.mylog.mylog import log, log_e
from commonlib.base_lib.utils.processpath import cur_file_dir


def get_cert_path(tmp_path=os.getcwd()):
    if tmp_path == os.path.dirname(tmp_path):
        log_e("can not find cert path")
        return ""
    if os.path.exists(os.path.join(tmp_path, "cert")) and os.path.isdir(os.path.join(tmp_path, "cert")):
        return os.path.join(tmp_path, "cert")
    else:
        return get_cert_path(os.path.dirname(tmp_path))


cert_dir = get_cert_path(os.path.join(__file__, ".."))
CA_CERT = os.path.join(cert_dir, "ca-chain.cert.pem")
KEY_FILE = os.path.join(cert_dir, "rccpclient.key")
CERT_FILE = os.path.join(cert_dir, "rccpclient.crt")


class RpcInterface(object):
    @staticmethod
    def exchange(ip, method, content, namespace, version='1.0', port=9000, timeout=60, cert_reqs=True, ca_certs=CA_CERT,
                 keyfile=KEY_FILE, certfile=CERT_FILE, **kwargs):
        log('<<<<<<<<<<<request data {0}'.format(content))
        log('<<<<<<<<<<<request api_name {0}'.format(method))
        log('<<<<<<<<<<<request  namespace {0}'.format(namespace))
        log('<<<<<<<<<<<request  ip {0}'.format(ip))
        res = rccpclient.call(addr=ip, method=method, namespace=namespace, content=content, version=version, port=port,
                              timeout=timeout, cert_reqs=cert_reqs, ca_certs=ca_certs, keyfile=keyfile,
                              certfile=certfile, **kwargs)
        result = res.content
        log('<<<<<<<<<<<<<<<response data {0}'.format(result))
        return json.loads(json.dumps(result, indent=2))


class RestfulInterface(object):
    @staticmethod
    def exchange(url, method, content, timeout=60, cert_reqs=True,
                 ca_certs=CA_CERT, keyfile=KEY_FILE, certfile=CERT_FILE, action=None, **kwargs):
        log('<<<<<<<<<<<request url {0}'.format(url))
        log('<<<<<<<<<<<request data {0}'.format(content))
        log('<<<<<<<<<<<request action {0}'.format(action))
        if method == "get":
            res = rccpclient.get(url=url, timeout=timeout, cert_reqs=cert_reqs,
                                 ca_certs=ca_certs, keyfile=keyfile, certfile=certfile, **kwargs)
        elif method == 'post':
            res = rccpclient.post(url=url, content=content, timeout=timeout, cert_reqs=cert_reqs,
                                  ca_certs=ca_certs, keyfile=keyfile, certfile=certfile, action=action, **kwargs)
        elif method == 'put':
            res = rccpclient.put(url=url, content=content, cert_reqs=cert_reqs, timeout=timeout,
                                 ca_certs=ca_certs, keyfile=keyfile, certfile=certfile, action=action, **kwargs)
        elif method == 'delete':
            res = rccpclient.delete(url=url, timeout=timeout, cert_reqs=cert_reqs, content=content,
                                    ca_certs=ca_certs, keyfile=keyfile, certfile=certfile, action=action, **kwargs)
        else:
            log("<<<<<<<<<<方法{}未定义".format(method))
            res = None
        result = res.content
        log('<<<<<<<<<<<<<<<response data {0}'.format(result))
        return json.loads(json.dumps(result, indent=2))


class NotifyInterface(object):
    @staticmethod
    def exchange(ip, event_type, content, publish_id, user='rcos', pwd='HHXX-ttxs-123', port=9000, timeout=60,
                 cert_reqs=True,
                 ca_certs=CA_CERT, keyfile=KEY_FILE, certfile=CERT_FILE, **kwargs):
        log('<<<<<<<<<<<request  ip {0}'.format(ip))
        log('<<<<<<<<<<<request data {0}'.format(content))
        log('<<<<<<<<<<<request  publish_id {0}'.format(publish_id))
        log('<<<<<<<<<<<request  event_type {0}'.format(event_type))
        res = rccpclient.notify(addr=ip, port=port, publish_id=publish_id, event_type=event_type, content=content,
                                timeout=timeout, cert_reqs=cert_reqs, ca_certs=ca_certs, keyfile=keyfile, user=user,
                                password=pwd,
                                certfile=certfile, **kwargs)
        result = res.content
        log('<<<<<<<<<<<<<<<response data {0}'.format(result))
        return json.loads(json.dumps(result, indent=2))


if __name__ == "__main__":
    rf = NotifyInterface()
    print(
        rf.exchange(ip='172.28.100.22', port=5671, event_type='node.heartbeat', publish_id='RCCPXuanyuan', content={}))
    pass
