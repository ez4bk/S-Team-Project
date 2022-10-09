# coding=utf-8
import json
import time

from commonlib.base_lib.ssh.ssh_info import SshInfo
from commonlib.base_lib.ssh.terminal_ssh import TerminalSsh
from websocket import create_connection, WebSocketTimeoutException, WebSocketConnectionClosedException
from commonlib.base_lib.mylog.mylog import log

url_model = "ws://{0}:{1}/shine/socket"
SHINE_PORT = 18710
SHINE_PATH = ['/etc/UserCfg/shine/shine_base.properties', '/usr/local/bin/config/shine_base.properties']

shine_instance = {}


def open_shine_port(ip, ssh_info=None):
    log("terminal start {} opne shine websocket port ".format(ip))
    if ssh_info is None:
        ssh = TerminalSsh(ip)
    else:
        ssh = TerminalSsh(ip, ssh_info=ssh_info)
    flag = False
    for item in SHINE_PATH:
        get_info_cmd = 'cat {} '.format(item)
        info = ssh.exec_command(get_info_cmd)
        if not info.__contains__('No such file or directory'):
            if info.__contains__('base.websocket.bind=true'):
                flag = True
                break
            else:
                cmd = "sed -i 's/base.websocket.bind=false/base.websocket.bind=true/' {0}".format(item)
                ssh.exec_command(cmd)
                log("terminal {} opne shine websocket port success".format(ip))
                ssh.exec_command('reboot')
                time.sleep(20)
                if wait_terminal_useful(ip, timeout=120, ssh_info=ssh_info):
                    return True
                else:
                    log(" terminal {} reboot fail")
                    flag = False
    return flag


def reboot_terminal(ip, ssh_info=None):
    log("terminal  {} reboot ".format(ip))
    if ssh_info is None:
        ssh = TerminalSsh(ip)
    else:
        ssh = TerminalSsh(ip, ssh_info=ssh_info)
    ssh.exec_command('reboot')
    if wait_terminal_useful(ip, timeout=60, ssh_info=ssh_info):
        return True
    else:
        log(" terminal {} reboot fail")
        return False


def wait_terminal_useful(ip, timeout=60, ssh_info=None):
    log("wait_terminal_useful>>>" + str(ip))
    ssh = TerminalSsh(ip, ssh_info=ssh_info)
    flag = False
    for i in range(timeout):
        flag = ssh.check_ssh()
        if flag is True:
            return flag
    return flag


class WebSocketInterface(object):

    def __get_ws(self, ip, timeout=10 * 1000, reconnect_flag=False, **kwargs):
        port = SHINE_PORT
        if "port" in kwargs:
            port = kwargs["port"]
        mark = self._get_mark_info(ip, port)
        if mark in shine_instance and not reconnect_flag:
            log(f"shine {ip} exist")
            return shine_instance[mark]
        else:
            log(f"create shine connect with ({ip, port})")
            url = url_model.format(ip, port)
            timeout = timeout / 1000
            ws = create_connection(url, timeout)
            shine_instance[mark] = ws
        return ws

    def exchange(self, ip, msg, timeout=10 * 1000, ssh_info=None, **kwargs):
        ws = self.__get_ws(ip, timeout=timeout, **kwargs)

        # status = ws.getstatus()
        # log(f"websocket {ip} status is " + str(status))
        key = str(kwargs.get("key"))

        data = json.dumps(msg)
        log("websocket data:" + str(data))
        try:
            ws.send(data)
        except:
            log("websocket destroy")
            ws = self.__get_ws(ip, timeout=timeout, reconnect_flag=True, **kwargs)
            ws.send(data)
        try:
            while True:
                result = ws.recv()
                result_json = json.loads(result)
                log(result_json)
                if result_json.get('action') == json.loads(data).get('action'):
                    break
                if key is not None and key in result_json.get('action'):
                    break
        except WebSocketTimeoutException:
            result = json.dumps({"code": 777, "message": "WebSocketTimeoutException"})
        except WebSocketConnectionClosedException:
            result = json.dumps({"code": 888, "message": "WebSocketConnectionClosedException"})
        # ws.close()
        return result

    def clear_websocket_buf(self, ip, **kwargs):
        port = SHINE_PORT
        if "port" in kwargs:
            port = kwargs["port"]
        mark = self._get_mark_info(ip, port)
        if mark in shine_instance:
            ws = shine_instance[mark]
            while True:
                try:
                    ws.recv()
                except WebSocketTimeoutException:
                    return
                except WebSocketConnectionClosedException:
                    return
        else:
            return

    def shine_receive_buf(self, ip, port):
        mark = self._get_mark_info(ip, port)
        if mark in shine_instance:
            ws = shine_instance[mark]
            while True:
                try:
                    result = ws.recv()
                except WebSocketTimeoutException:
                    result = json.dumps({"code": 777, "message": "WebSocketTimeoutException"})
                except WebSocketConnectionClosedException:
                    result = json.dumps({"code": 888, "message": "WebSocketConnectionClosedException"})
                return result
        else:
            raise Exception(f"shine {ip} is not connect")

    def _get_mark_info(self, ip, port):
        return fr"{ip}#{port}"


if __name__ == '__main__':
    pass
    msg = {}
    ssh_info = SshInfo("172.28.23.215", 10122, "rcd", "Rjrcd123@Admin123", "root", "rootRj369@Admin123")
    print(open_shine_port('172.28.23.215', ssh_info))
    msg["action"] = "request_language"
    msg["module"] = "shine"
    msg["timestamp"] = int(round(time.time() * 1000))
    # msg["action"] = "start_login"
    # msg["worker"] = "172.20.113.226"
    # msg["data"] = {"loginMode": "0", "userName": "userB", "password": "123456", "remember": "false"}
    # login_data = {"worker":"172.20.113.226","module":"shine","timestamp":"nowdate","action":"start_login","data":{"loginMode":"0","userName":"userB","password":"123456","remember":"false"}}
    # aa = WebSocketInterface()
    # for a in range(1):
    #     print(aa.exchange(ip='172.20.94.219', msg=msg))
    # time.sleep(1)
    #
    # print(aa.exchange(ip='172.20.94.219', msg=msg))
    # time.sleep(1)
    # msg["timestamp"] = int(round(time.time() * 1000))
    # print(aa.exchange(ip='172.20.94.219', msg=msg))
    # time.sleep(1)
    # msg["timestamp"] = int(round(time.time() * 1000))
    # print(aa.exchange(ip='172.20.94.219', msg=msg))
    # print(aa.exchange1(ip='172.20.94.219', msg=msg))
    # print(aa.exchange1(ip='172.20.94.219', msg=msg))
    # print(aa.exchange(ip='172.20.94.219', msg=msg))
    # print(aa.exchange1(ip='172.20.94.219', msg=msg))
    # print(aa.exchange1(ip='172.20.94.219', msg=msg))
    # print(aa.exchange1(ip='172.20.94.219', msg=msg))
    # print(aa.exchange(ip='172.20.94.219', msg=msg))
    # aa = {"code": 888}
    # json.loads(json.dumps({"code": 888}))
