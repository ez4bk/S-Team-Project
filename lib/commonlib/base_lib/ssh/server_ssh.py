# coding=utf-8
import re

import requests

from config import server_info
from lib.commonlib.base_lib.ssh import ssh_utils, ssh_security_utils
from lib.commonlib.base_lib.ssh.ssh_info import SshInfo
from lib.commonlib.base_lib.ssh.ssh_utils import SshUtils


def get_ssh_password(web_pwd, os_version, device_sn, login_url='http://172.28.92.151:9999/'):
    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
    }
    sss = requests.Session()
    r = sss.get(login_url, headers=my_headers)
    txt = r.content.decode()
    reg = '<form method=\'post\'>\n<input type=\'hidden\' name=\'csrfmiddlewaretoken\' value=\'(.*)\''
    pattern = re.findall(reg, txt)
    token = pattern[0]
    my_data = {
        'csrfmiddlewaretoken': token,
        'a': web_pwd,
        'b': os_version,
        'c': device_sn
    }
    # 登录后
    r = sss.post(login_url, headers=my_headers, data=my_data)
    reg = "密码：<br>(.*?)<br>"
    msg = r.text
    pattern = re.findall(reg, msg)
    ssh_pwd = pattern[0]
    return str(ssh_pwd).strip()


def open_authorize(server_ip, cookies):
    return ssh_security_utils.open_authorize(server_ip, cookies)


class ServerSsh(SshUtils):
    """
    SERVER SSH类，可以使用此类中的exec_command函数，在SERVER上执行指令

    ServerSsh构造在传入的ssh_info=None时，会根据server_ip去自动适配一个服务器的ssh用户名与密码（可能适配不到合适的ssh用户名与密码）

    当传入的ssh_info不为None时，即ssh_info = :py:class:`SshInfo()`.类时，将使用ssh_info中的配制信息进行数据库连接。
    """

    def __init__(self, device_ip, ssh_info=None, server_version="", server_sn="", web_pwd=""):
        super().__init__(device_ip, ssh_info)
        self._server_version = server_version
        self._server_sn = server_sn
        self._web_pwd = web_pwd

    def get_ssh_info(self, fix_flag=False):
        """
        获取服务器SSH连接的属性信息,类型为:py:class:`SshInfo()`.


        :return:返回SSH连接属性信息类
        """
        if not fix_flag:
            for a in server_info.ssh_info_list:
                if a.ip == self._ip:
                    self._ssh_info = a
                    return a
        if self._ssh_info is None:
            tmp = self._server_version
            if not self._server_version.startswith("RCO_V"):
                tmp = "RCO_V" + self._server_version
            if tmp >= "RCO_V4.1_R1P3":
                pwd = get_ssh_password(web_pwd=self._web_pwd, os_version=self._server_version,
                                       device_sn=self._server_sn)
                if tmp >= "RCO_V5.2":
                    self._ssh_info = SshInfo(self._ip, 9622, "root", pwd, "root", pwd)
                else:
                    self._ssh_info = SshInfo(self._ip, 22, "root", pwd, "root", pwd)
            else:
                self._ssh_info = ssh_utils.get_server_ssh_info(self._ip)
        return self._ssh_info

    def check_ssh(self):
        """
        确认SERVER是否连接成功，成功返回True,失败返回False

        :return: 成功返回True,失败返回False
        """
        return super().check_ssh()

    def exec_command(self, cmd, cmd_timeout=5 * 1000):
        """
        SERVER执行指令，返回执行结果。不支持阻塞式指令，如top等

        :param cmd: 指令内容
        :param cmd_timeout: 指令执行的超时时间

        :return: 返回执行结果
        """
        return super().exec_command(cmd, cmd_timeout)


if __name__ == '__main__':
    error_time = 0
    count = 0
    # for i in range(100 * 10000):
    #     tmp_client = ServerSsh("172.28.100.132", SshInfo("172.28.100.122", 9622, "root", "ruijie", "root", "ruijie"))
    #     try:
    #         tmp_client.exec_command("ls")
    #     except Exception:
    #         error_time += 1
    #     count += 1
    #     print(">>>count time :" + str(count))
    #     print(">>>error time :" + str(error_time))
    #     break
    tmp = ServerSsh("172.28.76.232", ssh_info=None, server_version="RCO_V4.1_R1P3.348", server_sn="G1LQB6B000081",
                    web_pwd="aaa")
    tmp.exec_command("ls")
