# coding=utf-8
from config import server_info
from lib.commonlib.base_lib.ssh import ssh_utils
from lib.commonlib.base_lib.ssh.server_ssh import ServerSsh
from lib.commonlib.base_lib.ssh.ssh_info import SshInfo
from lib.commonlib.base_lib.ssh.ssh_utils import SshUtils, connect_ssh


def get_security_terminal_ssh(server_ssh, terminal_ip):
    md5 = _get_server_md5(server_ssh)
    ssh_info = _get_security_terminal_ssh(terminal_ip, md5)
    ssh_client = connect_ssh(ssh_info.ip, ssh_info.port, ssh_info.user_name, ssh_info.user_pwd)
    if ssh_client is None:
        return None
    else:
        ssh_client.close()
        return ssh_info
    #     self._ssh_client = ssh_client


def _get_security_terminal_ssh(terminal_ip, md5):
    user_pwd = "Rjrcd123@" + str(md5)[0:32 - len("Rjrcd123@")]
    root_pwd = "rootRj369@" + str(md5)[0:32 - len("rootRj369@")]
    return SshInfo(terminal_ip, 10122, "rcd", user_pwd, "root", root_pwd)


def _get_server_md5(server_ssh_info):
    result = ServerSsh(server_ssh_info.ip, server_ssh_info).exec_command("cat /etc/.YmU1YzJhMjA")
    if str(result).__contains__("No such file or directory"):
        return ""
    return str(result).split("[")[0]


class TerminalSsh(SshUtils):
    """
    Terminal SSH类，可以使用此类中的exec_command函数，在SERVER上执行指令

    TerminalSsh构造在传入的ssh_info=None时，会根据server_ip去自动适配一个终端的ssh用户名与密码（可能适配不到合适的ssh用户名与密码）

    当传入的ssh_info不为None时，即ssh_info = :py:class:`SshInfo()`.类时，将使用ssh_info中的配制信息进行数据库连接。
    """

    def __init__(self, device_ip, ssh_info=None, server_ssh_info=None):
        super().__init__(device_ip, ssh_info)
        self._server_ssh_info = server_ssh_info

    # def _get_ssh(self):
    #     if self._ssh_info is None:
    #         self._ssh_info = get_terminal_ssh_info(self._ip)
    #         if self._ssh_info is None:
    #             return None
    #             # raise Exception("can not get server " + str(self._ip) + " server info")
    #     ssh_client = connect_ssh(self._ip, self._ssh_info.port, self._ssh_info.user_name,
    #                              self._ssh_info.user_pwd)
    #     self._ssh_client = ssh_client

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
            if self._server_ssh_info is not None:
                self._ssh_info = get_security_terminal_ssh(self._server_ssh_info, self._ip)
                if self._ssh_info is not None:
                    server_info.ssh_info_list.append(self._ssh_info)
                    return self._ssh_info
            self._ssh_info = ssh_utils.get_terminal_ssh_info(self._ip, fix_flag)

        return self._ssh_info

    # def check_ssh(self):
    #     """
    #     确认SERVER是否连接成功，成功返回True,失败返回False
    #
    #     :return: 成功返回True,失败返回False
    #     """
    #     return super().check_ssh()

    # def exec_command(self, cmd, cmd_timeout=5 * 1000):
    #     """
    #     SERVER执行指令，返回执行结果。不支持阻塞式指令，如top等
    #
    #     :param cmd: 指令内容
    #     :param cmd_timeout: 指令执行的超时时间
    #
    #     :return: 返回执行结果
    #     """
    #     return super().exec_command(cmd, cmd_timeout)


if __name__ == '__main__':
    tmp = ServerSsh("172.28.76.232", ssh_info=None, server_version="RCO_V4.1_R1P3.348", server_sn="G1LQB6B000081",
                    web_pwd="aaa").get_ssh_info()
    TerminalSsh("172.20.115.96", server_ssh_info=tmp).exec_command("ls /opt/lessons")
