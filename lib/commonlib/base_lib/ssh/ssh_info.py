# coding=utf-8


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

    def __init__(self, ip, port, user_name, user_pwd, root_name, root_pwd):
        self.ip = ip
        self.port = port
        self.user_name = user_name
        self.user_pwd = user_pwd
        self.root_name = root_name
        self.root_pwd = root_pwd

    def __str__(self) -> str:
        return self.ip + "," + str(self.port) + "," + str(self.user_name) + "," + str(self.user_pwd) + "," + str(
            self.root_name) + "," + str(self.root_pwd)
