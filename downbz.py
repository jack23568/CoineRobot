# coding : utf-8
import os
import json
import requests
import urllib
import time
import re

def downImage():

    path =os.path.join('image','WZIMG2')
    if not os.path.exists(path):
        os.makedirs(path)


    url_1 = 'http://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi?activityId=2735&sVerifyCode=ABCD&sDataType=JSON&iListNum=20&totalpage=0&page=0&iOrder=0&iSortNumClose=1&jsoncallback=jQuery17103959389879636743_1518353258597&iAMSActivityId=51991&_everyRead=true&iTypeId=2&iFlowId=267733&iActId=2735&iModuleId=2735&_=1518353258858'
    r =requests.get(url_1)

    html =r.content
    reg = r'jQuery17103959389879636743_1518353258597\((.*?)\)'
    result =re.findall(reg, html)
    json_result =json.loads(result[0])
    print type(json_result)
    #print json_result

    totalpage =int(json_result['iTotalPages'])
    totallines =json_result['iTotalLines']

    print totalpage,totallines

    image_list =json_result['List']
    print type(image_list)
    print len(image_list)
    
    for k in range(totalpage):
        url_2 = 'http://apps.game.qq.com/cgi-bin/ams/module/ishow/V1.0/query/workList_inc.cgi?activityId=2735&sVerifyCode=ABCD&sDataType=JSON&iListNum=20&totalpage=0&page=%s&iOrder=0&iSortNumClose=1&jsoncallback=jQuery17103959389879636743_1518353258597&iAMSActivityId=51991&_everyRead=true&iTypeId=2&iFlowId=267733&iActId=2735&iModuleId=2735&_=1518353258858' % k

        r =requests.get(url_2)

        html =r.content
        reg = r'jQuery17103959389879636743_1518353258597\((.*?)\)'
        result =re.findall(reg, html)
        json_result =json.loads(result[0])

        #print json_result
        
        image_list =json_result['List']

        for i in image_list:
            try:
                image_name =i['sProdName']
                image_url =i['sProdImgNo_6']
                image_name_true =urllib.unquote(image_name.encode('gbk')).decode('utf-8')
                image_url_dco =urllib.unquote(image_url)[:-3]
                print u'%s begin...' % image_name_true
                filepath =os.path.join(path,u'%s.gif' % image_name_true)
                if os.path.exists(filepath):
                    print u'Exists.... %s' % image_name_true
                    continue
                r =requests.get(image_url_dco)
                f =open(filepath, 'wb')
                f.write(r.content)
                f.close()
                print u'%s OK.' % image_name_true
            except:
                print u'%s Fail..' % image_name_true

if __name__ =='__main__':
    start =time.time()
    downImage()
    end =time.time()
    print end-start,u's'



