from bs4 import BeautifulSoup as bs
from urllib import request
import pandas as pd
import json
import DataBaseHomeWort_MongoDB as db

requrl = 'https://movie.douban.com/subject/26985127/comments'
url_attributes='?start=0&limit=20'
resp = request.urlopen(requrl+url_attributes)
html_data = resp.read().decode('utf-8') 
soup = bs(html_data, 'html.parser')

#获取到评论标签
comment_div_lits = soup.find_all('div', class_='comment')

#生成字典结构
data_dict = {'count':[],'username' : [],'watched' : [],'time' : [],'vote' : [],'comment' : []}
count = 1
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
#db.save(json.loads(data_frame.T.to_json()).values())

#获取下一页链接
paginator=soup.find_all('div', id='paginator')[0]
url_attributes=paginator.find_all('a', class_='next')[0]['href']
print(url_attributes)