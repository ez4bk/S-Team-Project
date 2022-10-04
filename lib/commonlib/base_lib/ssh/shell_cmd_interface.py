# coding=utf-8
import re
import socket
import time
import traceback
from abc import abstractmethod

from lib.commonlib.base_lib.mylog.mylog import _commonlib_log


class ShellCmdInterface(object):
    """
    SSH 抽象接口类，提供给终端SSH与服务器SSH进行具体实例
    """

    def __init__(self, device_ip):
        """
        :param device_ip:
        """
        self._ip = device_ip
        self._ssh_info = None

    @abstractmethod
    def exec_command(self, cmd, cmd_timeout=3):
        pass

    @abstractmethod
    def _get_ssh(self):
        pass

    @abstractmethod
    def _close_ssh(self):
        pass

    @staticmethod
    def _close_ssh_do(client):
        if client is not None:
            try:
                client.close()
            except Exception:
                _commonlib_log(traceback.format_exc())

    def _chanel_root(self, chanel_ssh_ob, pwd):
        result = self.__cmd_whoami(chanel_ssh_ob)
        if str(result).__contains__("~$"):
            _commonlib_log("change ssh root by pwd " + str(pwd))
            cmd = 'su root'
            chanel_ssh_ob.send(cmd)
            chanel_ssh_ob.send("\n")
            for a in range(3):
                time.sleep(0.1)
                result = chanel_ssh_ob.recv(9999).decode("utf8")
                if result.endswith("Password: "):
                    return self.__input_password(chanel_ssh_ob, pwd)
        return True

    def __input_password(self, chanel_ssh_ob, pwd, timeout=10 * 1000):
        chanel_ssh_ob.send(pwd)
        chanel_ssh_ob.send("\n")
        result = ""
        begin = time.time()
        time.sleep(0.1)
        while True:
            resp = chanel_ssh_ob.recv(9999).decode("utf8")
            result += resp
            if self.__check_cmd_end(resp):
                if result.__contains__("failure"):
                    _commonlib_log("ssh password is " + str(pwd))
                    _commonlib_log(result)
                    return False
                else:
                    return True
            else:
                time.sleep(1)
            if time.time() - begin >= timeout / 1000 + 1:
                return False

    def __cmd_whoami(self, chanel_ssh_ob, timeout=10 * 1000):
        cmd = "whoami"
        chanel_ssh_ob.send(cmd)
        chanel_ssh_ob.send("\n")
        result = ""
        begin = time.time()
        time.sleep(0.1)
        while True:
            resp = chanel_ssh_ob.recv(9999).decode("utf8")
            result += resp
            flag, cmd_user = self.__check_cmd_end(resp)
            if flag and result.__contains__(cmd_user + " whoami"):
                tmp = self.ssh_result_parse(result, cmd, cmd_user)
                return "".join(tmp)
            else:
                time.sleep(1)
            if time.time() - begin >= timeout / 1000 + 1:
                _commonlib_log("!!!shell cmd " + str(cmd) + " timeout")
                return None

    def _simple_ssh_cmd(self, chanel_ssh_ob, cmd, timeout=10 * 1000, process_callback=None):
        chanel_ssh_ob.send(cmd)
        chanel_ssh_ob.send("\n")
        result = ""
        begin = time.time()
        time.sleep(0.1)
        while True:
            try:
                resp = chanel_ssh_ob.recv(9999).decode("utf8")
            except socket.timeout:
                _commonlib_log("!!!shell cmd " + str(cmd) + " timeout")
                return None
            result += resp
            if process_callback is not None:
                process_callback(chanel_ssh_ob, resp)
            flag, cmd_user = self.__check_cmd_end(resp)
            if flag:
                tmp = self.ssh_result_parse(result, cmd, cmd_user)
                return "".join(tmp)
            else:
                time.sleep(1)
            if time.time() - begin >= timeout / 1000 + 1:
                _commonlib_log("!!!shell cmd " + str(cmd) + " timeout")
                return None

    @staticmethod
    def __check_cmd_end(resp):
        # a = re.findall('@RainOS:', resp)
        # b = re.findall('@RCD', resp)
        resp = str(resp).strip()
        c = re.findall('(.*@.*:.*#$)', resp)
        d = re.findall('(.*@.*:.*\$$)', resp)
        e = re.findall('(\[.*@.*.*\]\$$)', resp)
        f = re.findall('(\[.*@.*.*\]#$)', resp)
        # if len(a) > 0 or len(b) > 0 or len(c) > 0 or len(d) > 0:
        if len(c) > 0:
            return True, c[0]
        if len(d) > 0:
            return True, d[0]
        if len(e) > 0:
            return True, e[0]
        if len(f) > 0:
            return True, f[0]
        return False, ""

    @staticmethod
    def ssh_result_parse(result, cmd, cmd_user):
        if cmd == "whoami":
            return result
        _commonlib_log("<<<<<<<<<<<<<<")
        _commonlib_log("\r" + result)
        _commonlib_log(">>>>>>>>>>>>>>>")
        _commonlib_log(result.encode())
        tmp_list = result.encode().split(b"\r\n")
        if tmp_list[-1].decode().startswith(cmd_user):
            result = tmp_list[1:-1]
        else:
            result = tmp_list[1:]  # 场景 47bce5c74f589f4867dbd57e9ca9f808[root@RCD ~]#
        if len(result) > 0 and result[0].decode().startswith(cmd_user + " " + cmd):
            result = result[1:]
        tmp = ""
        for a in result:
            tmp += a.decode()
            tmp += "\r\n"
        if len(result) > 0:
            tmp = tmp[:-2]
        ret = re.sub("\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]", "", tmp)
        # tmp = "\r\n".join(result)
        # if result.encode().__contains__(cmd.encode()):
        #     data = re.findall("(?s).*@.*?#.*?" + cmd + "\r", result)
        #     if len(data) > 0:
        #         result = result[len(data[0]):]
        #         tmp = result.split("\r")[:-1]
        #     else:
        #         tmp = result.split("\r")[1:-1]
        # else:
        #     tmp = result.split("\r")[1:-1]
        #
        # if len(tmp) > 0:
        #     if tmp[0].startswith("\n"):
        #         tmp[0] = tmp[0][1:]
        #     if tmp[-1].endswith("\n"):
        #         tmp[-1] = tmp[-1][:-1]
        return ret
