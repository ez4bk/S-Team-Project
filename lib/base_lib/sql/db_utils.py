import time

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sshtunnel import SSHTunnelForwarder

from lib.base_lib.mylog.mylog import _commonlib_log


class DbUtils:
    def __init__(self):

        self.client = ""
        self.server = None

    def connect(self, host_ip):
        for a in range(3):
            try:
                self.server = SSHTunnelForwarder(
                    ssh_address_or_host=(host_ip, 22),  # B机器的配置
                    ssh_password="MjI1ZDY2NjQ",
                    ssh_username="root",
                    remote_bind_address=('127.0.0.1', 5433)
                )

                self.server.start()

                self.client = psycopg2.connect(database="rcd",
                                               user="postgres",
                                               password="MjI1ZDY2NjQ",
                                               host='127.0.0.1',
                                               # 因为上面没有设置 local_bind_address,所以这里必须是127.0.0.1,如果设置了，取设置的值就行了。
                                               port=self.server.local_bind_port)  # 这里端口也一样，上面的server可以设置，没设置取这个就行了
                return True

            except Exception as msg:
                print(str(msg))
                self.disconnect()
                time.sleep(5)
        return False

    def disconnect(self):
        try:
            self.client.close()
            self.server.stop()
        except Exception as msg:
            print(str(msg))

    def select_info(self, mysql):
        try:
            cur = self.client.cursor()
            print(mysql)
            cur.execute(mysql)
            rows = cur.fetchall()
            return rows
        except Exception as msg:
            print(str(msg))

    # def UpdataInfo(self, mysql):
    #     cur = self.client.cursor()
    #     cur.execute(mysql)
    #     self.client.commit()


def server_sql_qurey(sshhost, sql, port=5433, qureresult=1, ssh_password="", ssh_port="MjI1ZDY2NjQ"):
    """连接postgresql数据库，并执行sql语句,1表示返回执行结果，0 表示不返回执行结果"""
    try:
        server = SSHTunnelForwarder(
            ssh_address_or_host=(sshhost, 22),  # B机器的配置
            ssh_password="MjI1ZDY2NjQ",
            ssh_username="root",
            remote_bind_address=('127.0.0.1', 5433)
        )

        server.start()

        _commonlib_log('Server connected via SSH')

        local_port = str(server.local_bind_port)
        print(local_port)
        engine = create_engine('postgresql://postgres:rcd3000@localhost:' + local_port + '/rcd', poolclass=NullPool)
        Session = sessionmaker(bind=engine)
        session = Session()
        print("1111111111111")
        aa = session.get_bind()
        print(aa)
        result = session.execute(sql)
        a = []
        for i in result:
            a.append(i)
        result.close()
        session.close()
        session.close_all()
        print(a)
        print("ccccccccc")
    except Exception as e:
        print(e)
        _commonlib_log("数据库异常请检查")
    finally:
        print("aaaaaaaaaaaaa")

        server.close()
        server.stop()
        print("bbbbbbbbbbbbb")
    print("22222222222222222")


if __name__ == '__main__':
    # db_utils = DbUtils()
    # db_utils.connect("172.28.100.112")
    # sql_cmd = "select vm_ip from idv_terminal where terminal_mac LIKE '%" + terminal_mac + "%'"
    sql_cmd = "select user_name from lb_seat_info"
    # result = db_utils.select_info(sql_cmd)
    # db_utils.disconnect()
    # print(result)
    # debug = DbUtils()
    # debug.connect("172.21.195.52")

    # debug.disconnect()

    server_sql_qurey("172.28.100.112", sql_cmd)
    print("333333333333333")
