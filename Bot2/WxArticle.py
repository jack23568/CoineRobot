# -*- coding: utf-8 -*-
import schedule
import re
import requests
import time
import threading
from Yzm import Chaojiying_Client
chaojiying = Chaojiying_Client('dageda', 'dageda', '1104')

'''
schedule  函数
# schedule.every().hour.do(job)  #小时
# schedule.every().day.at("10:30").do(job)   #确定时间
# schedule.every(5).to(10).days.do(job)   #5到10天
# schedule.every().monday.do(job)   #一个月
# schedule.every().wednesday.at("13:15").do(job)  #每个星期
#schedule.every(1).minutes.do(job)  #每分钟
'''
import Article
from dao import *
articleDao =ArticleDao()

def get_url(url):
    '''
    重构文章的url  获取四个参数 _biz mid idx sn
    :param url: 微信公众号原生的url
    :return: 重构的url
    '''
    try:
        result=re.findall(r'_biz=(.*?)&.*mid=(.*?)&.*idx=(.*?)&.*sn=(.*?)&',url,re.S)
        __biz,mid,idx,sn=result[0]
        new_url='http://mp.weixin.qq.com/s?__biz={0}&mid={1}&idx={2}&sn={3}'.format(__biz,mid,idx,sn)
        return new_url
    except Exception as e:
        return 0

def get_proxy():
    '''
    获取代理IP  暂时不可用
    :return: 
    '''
    url='http://120.79.64.206/api/proxy/?num=10&scheme=HTTP&anonymity=anonymous'
    res=requests.get(url=url)
    proxy = {"http": res.json()['data']['detail'][0]['url']}
    return proxy

def get_code():
        '''
        获取验证码 手动输入的 注意Python3.6版本的
        :return: 
        '''
        t= lambda: int(round(time.time() * 1000))
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.81 Safari/537.36',
            'Host': 'www.digudata.com',
        }
        url='http://www.digudata.com/captcha?{}'.format(t)
        session=requests.session()
        res=session.get(url=url,headers=headers)
        with open('yzm.jpg','wb') as f:
            f.write(res.content)
        im = open('yzm.jpg', 'rb').read()
        code=chaojiying.PostPic(im, 1104).get('pic_str')
        return code,session

def parse_html(search_url,**kwargs):
    '''
    解析网页 获取点赞量,阅读数
    :param url: 
    :return: 
    '''
    try:
        code=kwargs.get('captcha','')    #获取验证码
        session=kwargs.get('session',None)  #获取验证码的Session
        headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.digudata.com',
            'Origin': 'http://www.digudata.com',
            'Referer': 'http://www.digudata.com/cmall/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.81 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        search_url=get_url(url=search_url)  #判断URL 是否合法  不合法为0
        if search_url:
            data = {
                'urlList[]': search_url,
                'platform': 'Wechat',
                'captcha': code
            }
            url = 'http://www.digudata.com/cmall/urlList/compute'
            if session!=None:
                r1 = session.post(url=url, data=data, timeout=10)
            else:
                r1=requests.post(url=url, data=data,headers=headers, timeout=10)
            result= r1.json()
            dict={'likes':'','reads':''}
            if result['success']==True:
                dict['likes']=result['result_list'][0]['likeNum']
                dict['reads']=result['result_list'][0]['readNum']
                return dict
            else:
                if u'验证码' in  result['message']:
                    captcha,session=get_code()
                    return parse_html(search_url=search_url,captcha=captcha,session=session)  #出现验证码 需要手动输入验证码查询
                else:
                    return result['message']
        else:
            return u'采集失败'
    except Exception as e:
         return u'采集失败 {}'.format(e)
    finally:
        if session!=None:
            session.close()  #关闭Session

def update():
    '''
    定时更新操作 ,从数据库中获取一系列的待更新URL
    然后将更新信息保存到数据库中
    :param article_list: 待更新URL
    :return: 
    '''
    # article_list='从数据库函数中返回待更新的URL列表'
    # for url in article_list:
    #         time.sleep(300)
    try:
        times = time.localtime(time.time()-24*60*60)
        lastdate = "%s%02d%s" % (times[0], int(times[1]), times[2])
        #article_tuple = articleDao.getArticleByDate(lastdate)
        article_tuple = articleDao.getAllArticle()
        article_list = []

        for tuple_ in article_tuple:
                list_ = []
                for _ in tuple_:
                    list_.append(_)
                if list_[3] !="":
                    article_list.append(list_)

        list_update = []
        print article_list
        for list__ in article_list:
            print list__[3]
            result = parse_html(list__[3])
            if isinstance(result, dict):
                list__[-3] = result['reads']
                list__[-2] = result['likes']

                print 'success'
            else:
                print 'error'
                print result
            list_update.append(list__)
            time.sleep(30)

        print list_update
        for a in list_update:
            article = Article.Article()
            article.id = a[0]
            article.article_name = a[1]
            article.article_title = a[2]
            article.article_url = a[3]
            article.read = a[4]
            article.like = a[5]
            article.last_edit_time = a[6]
            articleDao.modifyArticle(article)
        print "update success"
    except Exception as e:
        print e.message


def listing():
    schedule.every(10).minutes.do(update)
    while True:
        schedule.run_pending()

threading.Thread(target=listing).start()
