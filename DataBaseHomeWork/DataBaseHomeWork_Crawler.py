from bs4 import BeautifulSoup as bs
from urllib import request
import pandas as pd
import json
import DataBaseHomeWort_MongoDB as db
from time import sleep

#设置请求头和cookie
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
cookie = 'bid=AMh4OmCIzZE; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.553986712.1539349049.1539349049.1539349049.1; __utmc=30149280; __utmz=30149280.1539349049.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=223695111.761399391.1539349049.1539349049.1539349049.1; __utmb=223695111.0.10.1539349049; __utmc=223695111; __utmz=223695111.1539349049.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; as="https://movie.douban.com/subject/26985127/comments?start=480&limit=20&sort=new_score&status=P"; ps=y; __utmb=30149280.2.10.1539349049; dbcl2="181416385:66lwd/0i4wU"; ck=L1Av; _pk_id.100001.4cf6=3630892148d8537a.1539349049.1.1539349099.1539349049.; push_noty_num=0; push_doumail_num=0'
headers = {"User-Agent":user_agent,"Cookie":cookie}

#设置链接
requrl = 'https://movie.douban.com/subject/26985127/comments'
url_attributes = '?start=0&limit=20'

#设置计数器
count = 1

while True:
    req = request.Request(requrl + url_attributes,headers=headers)
    resp = request.urlopen(req)
    html_data = resp.read().decode('utf-8') 
    soup = bs(html_data, 'html.parser')

    #获取到评论标签
    comment_div_lits = soup.find_all('div', class_='comment')

    #生成字典结构
    data_dict = {'count':[],'username' : [],'watched' : [],'time' : [],'vote' : [],'comment' : []}
    
    #解析html
    for item in comment_div_lits:
        info = item.find_all('span', class_='comment-info')[0]#获取评论信息标签
        username = info.a.get_text()#获取用户名
        watched = info.find_all('span', class_='')[0].get_text()#获取用户是否已经看过
        time = info.find_all('span', class_='comment-time')[0].get_text(strip=True)#获取评论时间
        vote = item.find_all('span', class_='votes')[0].get_text()#获取有用数
        comment = item.find_all('span', class_='short')[0].get_text()#获取正文

        #在字典中存入内容
        data_dict['count'].append(count)
        data_dict['username'].append(username)
        data_dict['watched'].append(watched)
        data_dict['time'].append(time)
        data_dict['vote'].append(vote)
        data_dict['comment'].append(comment)
        count = count + 1

    # 创建DataFrame
    columns = ['count','username', 'watched', 'time', 'vote', 'comment']
    index = [i for i in range(len(data_dict['count']))]
    data_frame = pd.DataFrame(data_dict, columns=columns, index=index)

    #将数据存入数据库
    db.save(json.loads(data_frame.T.to_json()).values())
    print(count)

    #获取下一页链接
    paginator = soup.find_all('div', id='paginator')[0]
    next = paginator.find_all('a', class_='next')
    
    #判断是否还有下一页
    if len(next) == 0:
        break

    url_attributes = next[0]['href']
    sleep(2)