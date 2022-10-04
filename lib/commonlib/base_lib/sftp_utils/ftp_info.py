# coding=utf-8


class FtpInfo(object):
    """
    FTP配制信息

    * ip            linux服务器IP
    * port          linux服务器端口
    * user_name     普通用户名
    * user_pwd      普通用户密码
    """

    def __init__(self, ip, port, user_name, user_password):
        self.ip = ip
        self.port = port
        self.user_name = user_name
        self.user_password = user_password
