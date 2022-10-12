# coding=utf-8
from config.server_info import SERVER_IP, SSH_PORT, SSH_USER, SSH_PWD


class SshInfo(object):
    """
    SSH 信息类，包含SSH连接时所需要的参数

    * ip            linux服务器IP
    * port          linux服务器端口
    * user_name     普通用户名
    * user_pwd      普通用户密码
    * root_name     超级管理员用户名
    * root_pwd      超级管理员密码

    """

    def __init__(self, ip=SERVER_IP, port=SSH_PORT, user_name=SSH_USER, user_pwd=SSH_PWD):
        self.ip = ip
        self.port = port
        self.user_name = user_name
        self.user_pwd = user_pwd

    def __str__(self) -> str:
        return self.ip + "," + str(self.port) + "," + str(self.user_name) + "," + str(self.user_pwd)
