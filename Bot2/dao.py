# coding:utf-8 
# @Time    : 2018/6/26 11:45
# @Author  : cjr
# @Email   : 2352404393@qq.com
# @File    : dao.py.py
# @Software: PyCharm
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from DBPool import *
import base64
from Loger import Log
logger=Log(app_name='dao')
log=logger.getlog()


class MessageDao(object):
    '''
    发言信息处理类
    '''
    def __init__(self):
        self.con = getConn();

    def addMessage(self, message):
        '''
        添加信息
        :param message: Message 对象
        :return :1 ->success,0->faild 
        '''

        message.text = base64.b64encode(message.text) # 使用base64编码保存数据，可以保存emoji

        sql = u"insert into tb_message(group_id, member, text, picture, recording,duration, create_time) " \
              u"values(%d, '%s', '%s', '%s', '%s', %d, '%s')" % \
              (message.group_id, message.member, message.text, message.picture, message.recording, message.duration, message.create_time)

        cursor = self.con.cursor()

        try:
            cursor.execute(sql)
            self.con.commit()
            return 1
        except Exception as e:
            self.con.rollback()
            log.error("MessageDao.addMessade: "+e.message)
            return 0

    def getMessage(self, id):
        '''
        根据id获取信息
        :param id: 信息ID
        :return: Message 对象 or NONE
        '''
        sql = u"select * from tb_message where id = %d " % id

        cursor = self.con.cursor()

        try:
            cursor.execute(sql)
            self.con.commit()
            res = cursor.fetchone()
            print res
            list = []
            for i in res:
                list.append(i)
            list[3] = base64.b64decode(list[3]) #从数据库解码得到原text
            return list

        except Exception as e:
            self.con.rollback()
            log.error("MessadeDao.Message: "+e.message)
            return None


class GroupDao(object):
    '''
    群数据操作类
    '''
    def __init__(self):
        self.con = getConn();

    def addGroup(self, group):
        '''
        添加群数据
        :param group: Group 对象
        :return: 1 ->success,2->faild 
        '''
        sql = u"insert into tb_group(group_name, number) values('{}', {})".format(group.group_name, group.number)

        cursor = self.con.cursor()

        try:
            cursor.execute(sql)
            self.con.commit()
            return 1
        except Exception as e:
            self.con.rollback()
            log.error("GroupDao.addGroup: "+e.message)
            return 0

    def modifyGroup(self, group):

        '''
        更新群信息
        :param group: Group对象
        :return: 1 ->success,2->faild 
        '''

        sql = u"update tb_group set group_name = '%s', number = %d where group_id = %d" % (group.group_name, group.number, group.group_id)
        cursor = self.con.cursor()

        try:
            cursor.execute(sql)
            self.con.commit()
            return 1
        except Exception as e:
            self.con.rollback()
            log.error("GroupDao.modifyGroup: "+e.message)
            return 0

    def removeGroup(self, group_id):
        '''
                删除群信息
                :param group: groud_id
                :return: 1 ->success,2->faild 
        '''
        sql = u"delete from  tb_group  where group_id = %r or group_name = '%r'" % (group_id, group_id)

        cursor = self.con.cursor()

        try:
            cursor.execute(sql)
            self.con.commit()
            return 1
        except Exception as e:
            self.con.rollback()
            log.error("GroupDao.removeGroup: "+e.message)
            return 0

    def findGroup(self,group_name):

        '''
                查询群信息
                :param group: group_name
                :return: Group对象 or None
        '''
        sql = u"select * from  tb_group  where  group_name = '%s'" % group_name

        cursor = self.con.cursor()

        try:
            cursor.execute(sql)
            self.con.commit()
            res = cursor.fetchone()
            return res
        except Exception as e:
            self.con.rollback()
            log.error("GroupDao.findGroup: "+ e.message)
            return None

class ArticleDao(object):
    def __init__(self):
        self.con = getConn();

    def addArticle(self, article):

        sql = u"insert into  tb_article(`article_name`,`article_title`,`article_url`,`read`,`like`,`last_edit_time`) " \
              u"values('%s','%s','%s',%d,%d,'%s')"\
              %(article.article_name,article.article_title, article.article_url, article.read, article.like, article.last_edit_time)

        cursor = self.con.cursor()

        try:
            cursor.execute(sql)
            self.con.commit()
            return 1
        except Exception as e:
            self.con.rollback()
            log.error("ArticleDao.addArticle: "+ e.message)
            return 0

    def getAllArticle(self):

        sql = u"select * from  tb_article "

        cursor = self.con.cursor()

        try:
            cursor.execute(sql)
            self.con.commit()
            res = cursor.fetchall()
            return res
        except Exception as e:
            self.con.rollback()
            log.error("AritcleDao.getAllArticle: "+ e.message)
            return None

    def getArticleByNameAndTitle(self,name,title):

        sql = u"select * from  tb_article where article_name = '%s' and article_title = '%s'"%(name, title)

        cursor = self.con.cursor()

        try:
            cursor.execute(sql)
            self.con.commit()
            res = cursor.fetchone()
            return res
        except Exception as e:
            self.con.rollback()
            log.error("ArticleDao.getArticleByNameAndTitle: "+e.message)
            return None

    def getArticleByDate(self,date):

        sql = u"select * from  tb_article where last_edit_time = '%s'"%date

        cursor = self.con.cursor()

        try:
            cursor.execute(sql)
            self.con.commit()
            res = cursor.fetchall()
            return res
        except Exception as e:
            self.con.rollback()
            log.error("ArticleDao.getArticleByDate: "+e.message)
            return None

    def modifyArticle(self, article):

        sql = u"update tb_article set `read` = %d , `like` = %d , last_edit_time = '%s'" \
              u" where id = %d" % (article.read, article.like, article.last_edit_time, article.id)

        cursor = self.con.cursor()

        try:
            cursor.execute(sql)
            self.con.commit()
            return 1
        except Exception as e:
            self.con.rollback()
            log.error("ArticleDao.modifyArticle: "+e.message)
            return 0

