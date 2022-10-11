# coding=utf-8
import traceback

import paramiko

from config.server_info import SERVER_IP
from lib.base_lib.mylog.mylog import log
from lib.base_lib.ssh.shell_cmd_interface import ShellCmdInterface
from lib.base_lib.ssh.ssh_info import SshInfo


def connect_ssh(host, port, user_name, password):
    for a in range(1):
        try:
            log("ssh connect with " + host + "/" + str(port) + " by " + user_name + "/" + password)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port, username=user_name, password=password, timeout=60)
            log("ssh connect " + host + " success")
            return client
        except Exception as e:
            log(e)
            log(traceback.format_exc())
    return None


class SshUtils(ShellCmdInterface):

    def __init__(self, server_ip=SERVER_IP, ssh_info=None):
        super().__init__(server_ip)
        self._ssh_client = None
        self._ssh_info = ssh_info
        self._channel_obj = None

    def get_ssh_info(self):
        """
        获取服务器SSH连接的属性信息,类型为SshInfo

        :return:返回SSH连接属性信息类
        """
        if self._ssh_info is None:
            self._ssh_info = SshInfo()
        return self._ssh_info

    def _get_ssh(self):
        self.get_ssh_info()
        if self._ssh_info is None:
            return None
        ssh_client = connect_ssh(self._ip, self._ssh_info.port, self._ssh_info.user_name,
                                 self._ssh_info.user_pwd)
        assert ssh_client is not None, f"SSH connection failed!"
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
        log("server ssh cmd: " + str(cmd))
        stdin, stdout, stderr = self._ssh_client.exec_command(cmd)
        result = str(stdout.read().decode("utf-8").strip())
        error = str(stderr.read().decode('utf-8').strip())
        assert error is not None, "Error in SSH executing command: {}".format(error)
        log("ssh result: %s" % result)
        self._close_ssh()
        return result

    def channel_destroy(self):
        self._channel_obj = None
        self._close_ssh()


if __name__ == "__main__":
    # from lib.commonlib.base_lib.ssh.ssh_utils import SSHUtils
    ssh_util = SshUtils()
    result_cmd = ssh_util.exec_command('ls')
    # ssh_util.check_ssh()
    # print(result)
