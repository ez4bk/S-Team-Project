# coding=utf-8
SERVER_IP = '127.0.0.1'

# Database Server Information
MYSQL_USER = 'root'
MYSQL_PWD = '123456'
MYSQL_DATABASE = 'FamiOwl'
MYSQL_PORT = 3307

mysql_server_config = {
    'host': SERVER_IP,
    'user': MYSQL_USER,
    'password': MYSQL_PWD,
    'database': MYSQL_DATABASE,
    'port': MYSQL_PORT,
}

# SSH Information
SSH_USER = 'ez4bk'
SSH_PWD = 'Wyc1qaz2wsx~'
SSH_ROOT = 'ez4bk'
SSH_ROOT_PWD = 'Wyc1qaz2wsx~'
SSH_PORT = 22

if __name__ == '__main__':
    import mysql.connector
    from lib.commonlib.base_lib.mylog.mylog import log

    cnx = mysql.connector.connect(**mysql_server_config)
    log("Connect")
    # mycursor = cnx.cursor()
    #
    # mycursor.execute("SELECT * FROM Penna")
    #
    # myresult = mycursor.fetchall()
    #
    # for x in myresult:
    #     print(x)
    cnx.close()
