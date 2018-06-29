# coding:utf-8 
# @Time    : 2018/6/26 10:40
# @Author  : cjr
# @Email   : 2352404393@qq.com
# @File    : DBPool.py
# @Software: PyCharm

import datetime
import pymysql
from DBUtils.PooledDB import PooledDB
import DBConfig

class DbManager():
    def __init__(self):
        try:
            self._pool = PooledDB(pymysql,5,host=DBConfig.host,user=DBConfig.user,passwd=DBConfig.passwd,db=DBConfig.db,port=DBConfig.port, use_unicode=True, charset="utf8mb4")
        except Exception as e:
            print "The parameters for DBUtils is:", ""

    def _getConn(self):
        return self._pool.connection()


_dbManager = DbManager()


def getConn():
    """ 获取数据库连接 """
    return _dbManager._getConn()


def _reConn():
    """ 重新连接数据库 """
    global _dbManager
    re = False
    try:
        _dbManager = DbManager()
        re = True
    except:
        import traceback
        traceback.print_exc()
    finally:
        return re

def reConn():
    print "%s: now try to reconnect Database!" % (datetime.datatime.now())
    flag = _reConn()
    if flag:
        print "%s reconnect database success!" % (datetime.datatime.now())
    else:
        print "%s reconnect database failed!" % (datetime.datatime.now())


