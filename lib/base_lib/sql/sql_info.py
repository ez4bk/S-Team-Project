# coding=utf-8
from config.server_info import MYSQL_USER, MYSQL_PWD, MYSQL_PORT, MYSQL_DATABASE


class SqlInfo(object):
    """
    SqlInfo 类用来配制连接数据库需要的参数

    * ssh_info :py:class:`SshInfo()` in :py:mod:`commonlib.base_lib.ssh.ssh_info`.
    * sql_user  连接数据使用的用户名称
    * sql_pwd   连接数据使用的用户密码
    * sql_port  数据库端口
    * sql_name  要连接的数据库名

    """

    def __init__(self, ssh_info=None, sql_user=MYSQL_USER, sql_pwd=MYSQL_PWD,
                 sql_port=MYSQL_PORT, sql_name=MYSQL_DATABASE):
        """
        :type ssh_info SshInfo
        :param ssh_info:
        :param sql_user:
        :param sql_pwd:
        :param sql_port:
        :param sql_name:
        """
        self.ssh_info = ssh_info
        self.sql_user = sql_user
        self.sql_pwd = sql_pwd
        self.sql_port = sql_port
        self.sql_name = sql_name
