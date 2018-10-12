from bs4 import BeautifulSoup as bs
from urllib import request
import DataBaseHomeWort_MongoDB as db

requrl = 'https://movie.douban.com/subject/26985127/comments' + '?' + 'start=0' + '&limit=20' 
resp = request.urlopen(requrl) 
html_data = resp.read().decode('utf-8') 
soup = bs(html_data, 'html.parser')

#获取到评论标签
comment_div_lits = soup.find_all('div', class_='comment')
print('haha')
for item in comment_div_lits:
    info = item.find_all('span', class_='comment-info')[0]#获取评论信息标签
    username = info.a.get_text()#获取用户名
    watched = info.find_all('span', class_='')[0].get_text()#获取用户是否已经看过
    time = info.find_all('span', class_='comment-time')[0].get_text(strip=True)#获取评论时间
    vote = item.find_all('span', class_='votes')[0].get_text()#获取有用数
    comment = item.find_all('span', class_='short')[0].get_text()#获取正文