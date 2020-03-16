# -*- coding:utf-8 -*-
# @Time     :2019/4/16 16:55
# @Author   :YIN
# @Email    :649626809@qq.com
# @File     :read_mysql.py
# @software :PyCharm
# from sshtunnel import SSHTunnelForwarder
import MySQLdb
import MySQLdb.cursors
import mysql.connector



def operation_mysql(sql):

    db_connect = MySQLdb.connect(host='',
                                 port=111,
                                 user="",
                                 passwd="",
                                 db="",
                                 cursorclass=MySQLdb.cursors.DictCursor,
                                 charset='utf8'
                                 )
    cursor = db_connect.cursor()
    cursor.execute(sql)
    db_connect.commit()
    data = cursor.fetchall()
    db_connect.close()
    # server.stop()
    return data


if __name__ == '__main__':
    sql = "SELECT username FROM bus_bsp.bsp_user LIMIT 1"
    res = operation_mysql(sql)
    print(res[0]["username"])
