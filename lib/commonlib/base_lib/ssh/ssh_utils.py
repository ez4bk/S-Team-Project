# coding=utf-8
import traceback

import paramiko

from config import server_info
from lib.commonlib.base_lib.mylog.mylog import _commonlib_log
from lib.commonlib.base_lib.ssh.shell_cmd_interface import ShellCmdInterface
from lib.commonlib.base_lib.ssh.ssh_info import SshInfo

"""
内部函数
"""


def get_terminal_ssh_info(server_ip, fix_flag=False):
    """
    终端连接

    :param fix_flag:
    :param server_ip: 要连接的终端IP
    :return: 返回连接终端使用的ssh_info信息
    """
    if not fix_flag:
        for a in server_info.ssh_info_list:
            if a.ip == server_ip:
                return a
    ssh_client = connect_ssh(server_ip, server_info.NEW_TERMINAL_SSH_PORT, server_info.TERMINAL_NEW_SSH_USER,
                             server_info.NEW_TERMINAL_SSH_PASSWORD)
    if ssh_client is not None:
        ssh_client.close()
        ssh_info = SshInfo(server_ip, server_info.NEW_TERMINAL_SSH_PORT, server_info.TERMINAL_NEW_SSH_USER,
                           server_info.NEW_TERMINAL_SSH_PASSWORD, "root", server_info.NEW_ROOT_TERMINAL_SSH_PASSWORD)
        server_info.ssh_info_list.append(ssh_info)
        return ssh_info
    ssh_client = connect_ssh(server_ip, server_info.TERMINAL_SSH_PORT, server_info.SERVER_SSH_USER,
                             server_info.TERMINAL_SSH_PASSWORD)
    if ssh_client is not None:
        ssh_client.close()
        ssh_info = SshInfo(server_ip, server_info.TERMINAL_SSH_PORT, server_info.SERVER_SSH_USER,
                           server_info.TERMINAL_SSH_PASSWORD,
                           "root", server_info.TERMINAL_SSH_PASSWORD)
        server_info.ssh_info_list.append(ssh_info)
        return ssh_info
    ssh_client = connect_ssh(server_ip, server_info.NEW_TERMINAL_SSH_PORT, server_info.TERMINAL_NEW_SSH_USER,
                             server_info.TERMINAL_SSH_PASSWORD)
    if ssh_client is not None:
        ssh_client.close()
        ssh_info = SshInfo(server_ip, server_info.NEW_TERMINAL_SSH_PORT, server_info.TERMINAL_NEW_SSH_USER,
                           server_info.TERMINAL_SSH_PASSWORD, "root", server_info.TERMINAL_SSH_PASSWORD)
        server_info.ssh_info_list.append(ssh_info)
        return ssh_info
    return None


def get_server_ssh_info(server_ip, fix_flag=False):
    if not fix_flag:
        for a in server_info.ssh_info_list:
            if a.ip == server_ip:
                return a
    ssh_client = connect_ssh(server_ip, server_info.SERVER_SSH_PORT, server_info.SERVER_SSH_USER,
                             server_info.DEFAULT_SERVER_PASSWORD_MjI)
    if ssh_client is not None:
        ssh_client.close()
        ssh_info = SshInfo(server_ip, server_info.SERVER_SSH_PORT, server_info.SERVER_SSH_USER,
                           server_info.DEFAULT_SERVER_PASSWORD_MjI,
                           server_info.SERVER_SSH_USER, server_info.DEFAULT_SERVER_PASSWORD_MjI)
        server_info.ssh_info_list.append(ssh_info)
        return ssh_info
    ssh_client = connect_ssh(server_ip, server_info.SERVER_SSH_PORT, server_info.SERVER_SSH_USER,
                             server_info.DEFAULT_SERVER_PASSWORD_35_)
    if ssh_client is not None:
        ssh_client.close()
        ssh_info = SshInfo(server_ip, server_info.SERVER_SSH_PORT, server_info.SERVER_SSH_USER,
                           server_info.DEFAULT_SERVER_PASSWORD_35_, server_info.SERVER_SSH_USER,
                           server_info.DEFAULT_SERVER_PASSWORD_35_)
        server_info.ssh_info_list.append(ssh_info)
        return ssh_info
    return None


def connect_ssh(host, port, user_name, password):
    for a in range(1):
        try:
            _commonlib_log("ssh connect with " + host + "/" + str(port) + " by " + user_name + "/" + password)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port, username=user_name, password=password, timeout=60)
            _commonlib_log("ssh connect " + host + " success")
            return client
        except:
            _commonlib_log(traceback.format_exc())
    return None


class SshUtils(ShellCmdInterface):

    def __init__(self, device_ip, ssh_info=None):
        super().__init__(device_ip)
        self._ssh_client = None
        self._ssh_info = ssh_info
        self._channel_obj = None

    def get_ssh_info(self, fix_flag=False):
        """
        获取服务器SSH连接的属性信息,类型为SshInfo

        :return:返回SSH连接属性信息类
        """
        if self._ssh_info is None:
            self._ssh_info = get_server_ssh_info(self._ip, fix_flag)
        return self._ssh_info

    def _get_ssh(self):
        self.get_ssh_info()
        if self._ssh_info is None:
            return None
        # raise Exception("can not get server " + str(self._ip) + " server info")
        ssh_client = connect_ssh(self._ip, self._ssh_info.port, self._ssh_info.user_name,
                                 self._ssh_info.user_pwd)
        if ssh_client is None:
            for a in server_info.ssh_info_list:
                if a.ip == self._ip:
                    server_info.ssh_info_list.remove(a)
                    return self._get_ssh()
        self._ssh_client = ssh_client

    def check_ssh(self):
        """
        确认SERVER是否连接成功，成功返回True,失败返回False

        :return: 成功返回True,失败返回False
        """
        self._get_ssh()
        if self._ssh_client is not None:
            self._close_ssh_do(self._ssh_client)
            return True
        return False

    def _close_ssh(self):
        self._close_ssh_do(self._ssh_client)

    def exec_command(self, cmd, cmd_timeout=5 * 1000):
        """
        SERVER执行指令，返回执行结果。不支持阻塞式指令，如top等

        :param cmd: 指令内容
        :param cmd_timeout: 指令执行的超时时间

        :return: 返回执行结果
        """
        self._get_ssh()
        if self._ssh_client is None:
            raise Exception("ssh can not connect server " + str(self._ip))
        _commonlib_log("server ssh cmd: " + str(cmd))
        chanel_ssh_ob = self._ssh_client.invoke_shell()  # 建立交互式的shell
        chanel_ssh_ob.settimeout(cmd_timeout / 1000 + 3)  # 设置接收与发送超时时间
        result = self._chanel_root(chanel_ssh_ob, self._ssh_info.root_pwd)
        if result:
            result = self._simple_ssh_cmd(chanel_ssh_ob, cmd, cmd_timeout)
        _commonlib_log("ssh result: \r" + str(result))
        self._close_ssh()
        return result

    def channel_exec_command(self, cmd, cmd_timeout=5 * 1000, process_callback=None):
        """

        :param cmd:
        :param cmd_timeout:
        :param process_callback:   函数原型：  def process_callback_func(channel,msg)
        :return:
        """
        if self._channel_obj is None:
            self._get_ssh()
            if self._ssh_client is None:
                raise Exception("ssh can not connect server " + str(self._ip))

            self._channel_obj = self._ssh_client.invoke_shell()  # 建立交互式的shell
            result = self._chanel_root(self._channel_obj, self._ssh_info.root_pwd)
        _commonlib_log("server ssh cmd: " + str(cmd))
        self._channel_obj.settimeout(cmd_timeout / 1000 + 3)  # 设置接收与发送超时时间
        result = self._simple_ssh_cmd(self._channel_obj, cmd, cmd_timeout, process_callback)
        _commonlib_log("ssh result: \r" + str(result))
        return result

    def channel_destroy(self):
        self._channel_obj = None
        self._close_ssh()
