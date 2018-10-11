from bs4 import BeautifulSoup as bs
from urllib import request

requrl = 'https://movie.douban.com/subject/26363254/comments' +'?' +'start=0' + '&limit=20' 
resp = request.urlopen(requrl) 
html_data = resp.read().decode('utf-8') 
soup = bs(html_data, 'html.parser') 
comment_div_lits = soup.find_all('div', class_='comment')

for item in comment_div_lits:
        print(item.find_all('span', class_='short')[0].get_text())