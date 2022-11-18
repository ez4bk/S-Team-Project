# coding=utf-8
from config.server_info import SSH_PORT, SERVER_IP, SSH_USER, SSH_PWD


class FtpInfo(object):
    """
    FTP配制信息

    * ip            linux服务器IP
    * port          linux服务器端口
    * user_name     普通用户名
    * user_pwd      普通用户密码
    """

    def __init__(self, ip=SERVER_IP, port=SSH_PORT, user_name=SSH_USER, user_pwd=SSH_PWD):
        self.ip = ip
        self.port = port
        self.user_name = user_name
        self.user_password = user_pwd
