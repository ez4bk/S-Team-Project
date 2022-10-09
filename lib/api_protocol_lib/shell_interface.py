# coding=utf-8
from commonlib.base_lib.ssh.server_ssh import ServerSsh


class ShellInterface(object):
    @staticmethod
    def exchange(server_ip, cmd, timeout=10 * 1000, **kwargs):
        server_ssh = ServerSsh(server_ip)
        result = server_ssh.exec_command(cmd, timeout)
        return result
