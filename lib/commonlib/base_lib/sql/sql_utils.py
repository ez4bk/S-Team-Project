# coding=utf-8
import traceback

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sshtunnel import SSHTunnelForwarder

from lib.commonlib.base_lib.mylog.mylog import _commonlib_log, _commonlib_log_e, log
from lib.commonlib.base_lib.sql.sql_info import SqlInfo
from lib.commonlib.base_lib.ssh.server_ssh import ServerSsh
from lib.commonlib.base_lib.ssh.ssh_info import SshInfo


class SqlUtils(object):
    """
    数据库操作，通过 sql_exec 接口可以实现对数据库的各种操作。

    SqlUtils构造在传入的sql_info=None时，会根据server_ip去自动适配一个服务器的ssh用户名与密码，再使用默认的
    sql_user="postgres", sql_pwd="rcd3000", sql_port=5433, sql_name="rcd" 进行数据库连接。

    当传入的sql_info不为None时，即sql_info = :py:class:`SqlInfo()`.类时，将使用ssh_info中的配制信息进行数据库连接。
    """

    def __init__(self, server_ip, sql_info=None):
        """
        :type   sql_info SqlInfo
        :param server_ip: 服务器IP地址
        """
        self.__server_ip = server_ip
        self.__sql_info = sql_info

    def __get_sql_info(self, sql_user="postgres", sql_pwd="rcd3000", sql_port=5433, sql_name="rcd"):
        if self.__sql_info is not None:
            return self.__sql_info
        else:
            server_ssh = ServerSsh(self.__server_ip)
            ssh_info = server_ssh.get_ssh_info()
            if ssh_info is None:
                return None
            return SqlInfo(ssh_info=ssh_info, sql_user=sql_user, sql_pwd=sql_pwd, sql_port=sql_port, sql_name=sql_name)

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
        _commonlib_log("sql_exec cmd>>>" + str(sql_cmd))
        if sql_info.ssh_info.port == 9622:  # 在新平台上使用 psycopg2
            return self.__sql_cmd_exec(sql_info, sql_cmd, result_flag)
        else:
            return self.__sql_cmd_exec_by_ssh(sql_info, sql_cmd, result_flag)

    @staticmethod
    def __sql_connect(sql_info):
        for a in range(3):
            try:
                conn = psycopg2.connect(database=sql_info.sql_name, user=sql_info.sql_user, password=sql_info.sql_pwd,
                                        host=sql_info.ssh_info.ip,
                                        port=sql_info.sql_port)
                return conn
            except Exception:
                _commonlib_log(traceback.format_exc())
        return None

    def __sql_cmd_exec(self, sql_info, sql_cmd, result_flag=1):
        """
        :type sql_info SqlInfo
        :param sql_info:
        :param result_flag:
        :return:
        """
        conn = None
        try:
            conn = self.__sql_connect(sql_info)
            cursor = conn.cursor()
            cursor.execute(sql_cmd)

            if result_flag == 1:
                rows = cursor.fetchall()
                log(str(rows))
                return rows
            else:
                conn.commit()
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def __sql_cmd_exec_by_ssh(self, sql_info, sql_cmd, result_flag=1):
        """
        :type sql_info SqlInfo
        :param sql_info:
        :param result_flag:
        :return:
        """
        server = None
        try:
            server = SSHTunnelForwarder(
                ssh_address_or_host=(sql_info.ssh_info.ip, sql_info.ssh_info.port),  # B机器的配置
                ssh_password=sql_info.ssh_info.root_pwd,
                ssh_username=sql_info.ssh_info.root_name,
                remote_bind_address=("127.0.0.1", int(sql_info.sql_port))
            )
            server.start()
            local_port = str(server.local_bind_port)
            return self.__sql_engine_exec(sql_info, sql_cmd, bind_port=local_port, result_flag=result_flag)
        except Exception as e:
            _commonlib_log_e(traceback.format_exc())
            raise e
        finally:
            server.stop()
            server.close()

    @staticmethod
    def __sql_engine_exec(sql_info, sql_cmd, bind_port, result_flag=1):
        session = None
        try:
            engine = create_engine(
                'postgresql://{0}:{1}@localhost:{2}/{3}'.format(sql_info.sql_user, sql_info.sql_pwd, bind_port,
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
                _commonlib_log("sql ret:" + str(a))
                return a
        except Exception as e:
            _commonlib_log(traceback.format_exc())
            if session is not None:
                session.rollback()
                session.close()
            raise e
        finally:
            session.close()

    def selectOperate(self):
        conn = psycopg2.connect(database="dayudb", user="dayuuser", password="Thank-Y0U", host="172.28.100.132",
                                port="5432")

        cursor = conn.cursor()
        cursor.execute("select vswitch_id,name,description,vswitch_type,vlan_id,state from t_dayu_vswitch")
        rows = cursor.fetchall()
        for row in rows:
            print(row[0])
        conn.close()


if __name__ == '__main__':
    tmp_ssh_info = SshInfo("172.28.100.132", 9622, "root", "rujie", "root", "ruijie")
    tmp_sql_info = SqlInfo(tmp_ssh_info, "dayuuser", "Thank-Y0U", "5432", "dayudb")
    index = 0
    while True:
        print("excust time>>>" + str(index))
        aa = SqlUtils("172.28.100.132", tmp_sql_info)
        sql = "select vswitch_id,name,description,vswitch_type,vlan_id,state from t_dayu_vswitch;"
        aa.sql_exec(sql, 1)
        # index += 1
        break
