# coding=utf-8
import traceback
from abc import abstractmethod

from lib.base_lib.mylog.mylog import log


class ShellCmdInterface(object):
    """
    SSH 抽象接口类，提供给终端SSH与服务器SSH进行具体实例
    """

    def __init__(self, server_ip):
        """
        :param server_ip:
        """
        self._ip = server_ip
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
                log(traceback.format_exc())


if __name__ == "__main__":
    pass
