# coding=utf-8
import traceback

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sshtunnel import SSHTunnelForwarder

from config.server_info import SERVER_IP
from lib.base_lib.mylog.mylog import log, log_e
from lib.base_lib.sql.sql_info import SqlInfo
from lib.base_lib.ssh.ssh_utils import SshUtils


class SqlUtils(object):
    """
    数据库操作，通过 sql_exec 接口可以实现对数据库的各种操作。

    SqlUtils构造在传入的sql_info=None时，会根据server_ip去自动适配一个服务器的ssh用户名与密码，再使用默认的
    sql_user="postgres", sql_pwd="rcd3000", sql_port=5433, sql_name="rcd" 进行数据库连接。

    当传入的sql_info不为None时，即sql_info = :py:class:`SqlInfo()`.类时，将使用ssh_info中的配制信息进行数据库连接。
    """

    def __init__(self, server_ip=SERVER_IP, sql_info=None):
        """
        Initialization function
        :type   sql_info SqlInfo
        :param server_ip: 服务器IP地址
        """
        self.__server_ip = server_ip
        self.__sql_info = sql_info

    def __get_sql_info(self):
        if self.__sql_info is not None:
            return self.__sql_info
        else:
            server_ssh = SshUtils(self.__server_ip)
            ssh_info = server_ssh.get_ssh_info()
            if ssh_info is None:
                return None
            return SqlInfo(ssh_info=ssh_info)

    def __sql_cmd_exec_by_ssh(self, sql_info, sql_cmd, result_flag=1):
        """
        Execute SQL query using SSH Tunnel
        :type sql_info: SqlInfo
        :param sql_info: MYSQL connection information
        :param sql_cmd: Query command to execute on the database
        :param result_flag: 1 for return value, 0 for no return value
        :return: return value or None
        """
        tunnel = None
        try:
            tunnel = SSHTunnelForwarder(
                ssh_address_or_host=(sql_info.ssh_info.ip, sql_info.ssh_info.port),
                ssh_password=sql_info.ssh_info.user_pwd,
                ssh_username=sql_info.ssh_info.user_name,
                remote_bind_address=(self.__server_ip, sql_info.sql_port)
            )
            tunnel.start()
            return self.__sql_engine_exec(sql_info, sql_cmd, bind_port=sql_info.sql_port, result_flag=result_flag)
        except Exception as e:
            log_e(traceback.format_exc())
            raise e
        finally:
            tunnel.stop()
            tunnel.close()

    @staticmethod
    def __sql_engine_exec(sql_info, sql_cmd, bind_port, result_flag=1):
        session = None
        try:
            engine = create_engine(
                'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(sql_info.sql_user,
                                                             sql_info.sql_pwd,
                                                             SERVER_IP,
                                                             bind_port,
                                                             sql_info.sql_name), poolclass=NullPool)
            Session = sessionmaker(bind=engine)
            session = Session()
            if result_flag == 0:
                session.execute(sql_cmd)
                session.commit()
            else:
                result = session.execute(sql_cmd)
                a = []
                for i in result:
                    a.append(i)
                result.close()
                log("SQL Return:" + str(a))
                return a
        except Exception as e:
            log(traceback.format_exc())
            if session is not None:
                session.rollback()
                session.close()
            raise e
        finally:
            session.close()

    def get_sql_info(self):
        """
        获取数据库的连接配制信息

        :return:    返回sql连接使用的配制信息,返回的为SshInfo类
        """
        return self.__get_sql_info()

    def sql_exec(self, sql_cmd, result_flag=1):
        """
        执行数据库指令，通过result_flag来判断是否需要返回信息，当result_flag = 0 时，返回None，当result_flag != 0时，返回执行结果，结果为数组元组

        :param sql_cmd: 要执行的sql指令
        :param result_flag: 当result_flag = 0 时，返回None，当result_flag != 0时，返回执行结果

        :return: 由result_flag决定是否返回信息
        """
        sql_info = self.__get_sql_info()
        if sql_info is None:
            raise Exception("can not get sql info")
        log("sql_exec cmd>>>" + str(sql_cmd))
        return self.__sql_cmd_exec_by_ssh(sql_info, sql_cmd, result_flag)


if __name__ == '__main__':
    aa = SqlUtils()
    sql = "select * from parents;"
    aa.sql_exec(sql, 1)
