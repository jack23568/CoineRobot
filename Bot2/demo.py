# coding:utf-8 
# @Time    : 2018/6/25 15:47
# @Author  : cjr
# @Email   : 2352404393@qq.com
# @File    : demo.py
# @Software: PyCharm

import os
import math
import time
import requests
from wxpy import *
from dao import *
import Groups
import Messages
import Article
import WxArticle
import schedule
import threading
import logging
groupDao= GroupDao()
messageDao = MessageDao()
articleDao = ArticleDao()
apply_msgDao=ApplyMessageDao()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('Info.log')
file_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

start_flag=True
group_id = 0

bot=None
def login_c():
    logger.info('bot start success')

while True:
    msg = apply_msgDao.get_message()
    if start_flag and msg=='1':
        bot = Bot(login_callback=login_c())
        start_flag=False
        break

def logout():
    msg = apply_msgDao.get_message()
    global start_flag,bot
    if start_flag == False and msg == '0':
        start_flag = True
        logging.info('bot logout()')
        bot.logout()
    elif start_flag ==True and msg == '0':
        while True:
            msg = apply_msgDao.get_message()
            if start_flag and msg == '1':
                bot = Bot(login_callback=login_c())
                start_flag = False
                register(bot)
                embed()
                break


def runing2():
    schedule.every(30).seconds.do(logout)   #30秒
    while True:
        schedule.run_pending()

# threading.Thread(target=runing).start()

flag = True

def register(bot):
    # 个人消息处理
    @bot.register(Friend)
    def help(msg):
        print ("Friend")
        logger.info("in friend: ")
        logger.info(msg)
        try:
            if msg.chat.remark_name == 'Boss':
                send_group_msg(msg)
        except Exception as e:
            logger.error("in friend: "+e.message)

    # 公众号消息处理me
    @bot.register(MP)
    def print_mp_msg(msg):
        print ("MP")
        logger.info("in MP: ")
        logger.info(msg)
        try:
            if msg.type == SHARING:
                dict_msg = msg.raw  # 获取推送文章信息 dict
                article_name = msg.chat.name  # 获取公众号名称
                article_title = msg.text  # 文章标题
                sharing_rawurl = dict_msg['Url']
                times = time.localtime(dict_msg['CreateTime'])  # 发言时间戳
                dt = "%s%02d%s" % (times[0], int(times[1]), times[2])  # 格式化时间

                article = Article.Article()
                article.article_name = article_name
                article.article_title = article_title
                article.last_edit_time = dt

                logger.info("in MP.raw_url: "+ sharing_rawurl)

                article.article_url = sharing_rawurl
                result = WxArticle.parse_html(sharing_rawurl)
                if isinstance(result, dict):
                    article.read = result['reads']
                    article.like = result['likes']
                    articleDao.addArticle(article)
                else:
                    article.article_url = ""
                    articleDao.addArticle(article)
                print result
        except Exception as e:
            logger.error("in MP: "+e.message)

    def send_group_msg(msg):
        '''
        群转发推送消息 
        :param msg: 
        :return: 
        '''
        Group_List = bot.groups(update=True)
        for group in Group_List:
            time.sleep(15)
            msg.forward(group)


    def listen():
        '''
        监听服务器传来的消息
        :return: 
        '''
        global flag
        msg = apply_msgDao.get_message()
        if msg != '' and flag:
            flag = False
            logger.info(u'监听收到内容:{}'.format(msg))
            Group_List = bot.groups(update=True)
            for group in Group_List:
                logger.info(u'正在发送消息到{}'.format(group.name))
                time.sleep(5)
                group.send_msg(msg)
            apply_msgDao.clean()  # 发送完毕后清空消息
            flag = True

    def runing():
        schedule.every(120).seconds.do(listen)   #30秒
        while True:
            schedule.run_pending()

    threading.Thread(target=runing).start()

    def deal_reply(msg, **kwargs):
        keywords = kwargs.get('keywords', None)
        if keywords == None:
            keywords = msg.text
        keywords = keywords.strip()
        logger.info(u'查询关键词:{}'.format(keywords))
        if keywords[0] != '[':
            image_path = ''
            url = 'http://test2.bicoin.info/robot/autoReply?keyword={}&type=1'.format(keywords)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
            res = requests.get(url=url, headers=headers)
            data = res.json()
            print data
            if data['type'] == '2' and data['code']:
                image_url = data['data']['images']
                text = data['data']['reply']
                print text, image_url
                if image_url != '' and text != '':  # 图片文字并存
                    msg.chat.send(text)
                    res = requests.get(url=image_url)
                    image_path = u'image/{}.jpg'.format(keywords)
                    with open(image_path, 'wb') as f:
                        f.write(res.content)
                    msg.chat.send_image(image_path)
                elif image_url != '' and text == '':  # 只有图片
                    res = requests.get(url=image_url)
                    image_path = u'image/{}.jpg'.format(keywords)
                    with open(image_path, 'wb') as f:
                        f.write(res.content)
                    msg.chat.send_image(image_path)
                elif text != '' and image_url == '':  # 只有文本消息
                    msg.chat.send(text)

    # 打印所有*群聊*对象中的*文本*消息
    @bot.register(Group)
    def print_group_msg(msg):

        '''
        群聊信息处理
        :param msg: 
        :return: 
        '''

        print ("Group")
        logger.info("in Group: ")
        logger.info(msg)
        try:
            dict_msg = msg.raw  # message对象字典
            menber = dict_msg['ActualNickName']  # 发言人
            group_name = msg.chat.name  # 群名称
            times = time.localtime(dict_msg['CreateTime'])  # 发言时间戳
            dt = "%s-%s-%s %s:%s:%s" % (times[0], times[1], times[2], times[3], times[4], times[5])  # 格式化时间
            filename = dict_msg['FileName']  # 发送文件名称
            group = groupDao.findGroup(group_name)  # 获取当前群信息 主要是group_id
            # group_id = 0
            if group == None:  # 群在数据库中不存在，则添加新的群信息
                newgroup = Groups.Group()
                newgroup.group_name = group_name
                newgroup.number = len(msg.chat)
                groupDao.addGroup(newgroup)
                group_id = groupDao.findGroup(group_name)[0]
            else:
                group_id = group[0]
        except Exception as e:
            logger.error("in Group: "+e.message)

        message = Messages.Message()
        message.group_id = group_id
        message.member = menber
        message.create_time = dt

        try:
            if msg.type == TEXT:
                # 发言保存到数据库
                text = dict_msg['Content']  # 发言内容
                message.text = text
                messageDao.addMessage(message)

                if u"@%s" % bot.self.name in msg.text:  # @机器人信息
                    text_key = msg.text[len(u"@%s" % bot.self.name):]
                    print text_key
                    deal_reply(msg, keywords=text_key)

                else:  # 普通信息
                    deal_reply(msg)

            if msg.type == NOTE:
                group = msg.chat
                group.update_group(True)
                logger.info("in Group.NOTE: "+msg.text)
                # print len(group)
                # bot.groups()[0].update_group(True)

            if msg.type == RECORDING:
                # 记录录音
                if not os.path.exists("recording"):
                    os.mkdir("recording")
                filename = u"recording/%s" % filename
                msg.get_file(filename)  # filename 存储路径
                duration = int(math.ceil(dict_msg['VoiceLength'] / 1000))
                message.recording = filename
                message.duration = duration
                messageDao.addMessage(message)

            if msg.type == PICTURE:
                # 存储图片
                if not os.path.exists("image"):
                    os.mkdir("image")
                filename = u"image/%s" % filename
                msg.get_file(filename)  # filename 存储路径
                message.picture = filename
                messageDao.addMessage(message)

            if msg.type == ATTACHMENT:
                # 存储文件
                if not os.path.exists("file"):
                    os.mkdir("file")
                filename = u"file/%s" % filename
                msg.get_file(filename)  # filename 存储路径

            if msg.type == VIDEO:
                # 存储视频
                if not os.path.exists("video"):
                    os.mkdir("video")
                filename = u"video/%s" % filename
                msg.get_file(filename)  # filename 存储路径

            if msg.type == SHARING:
                pass
                print dict_msg['Url']

        except Exception as e:
            logger.error("in Group: " + e.message)

    threading.Thread(target=runing2).start()

    embed()


register(bot)


if __name__ == '__main__':

    pass


