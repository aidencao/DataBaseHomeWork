import MongoDB as db
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba.analyse
import re
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np

#设置中文字体
plt.rcParams['font.sans-serif'] = ['KaiTi']
plt.rcParams['font.serif'] = ['KaiTi']

def showstar():
    #从数据库获取数据
    data = pd.DataFrame(list(db.get()))

    #生成直方图
    data['star'].value_counts().plot.bar()
    plt.title(u'电影《一出好戏》评价分布')
    plt.show()

def getWordcloud_withimg():
    #从数据库获取数据
    data = pd.DataFrame(list(db.get()))
    data = data['comment']
    
    #将所有评论合并
    comments = ''
    for comment in data: 
        comments = comments + comment.strip()
    
    #去除评论中的标点
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, comments)
    cleaned_comments = ''.join(filterdata)
    
    #增加停止词
    jieba.analyse.set_stop_words(stop_words_path='chineseStopWords.txt')
    
    #分词
    keywords = jieba.analyse.extract_tags(cleaned_comments, topK=500, withWeight=True, allowPOS=())

    #设置背景图片
    background = np.array(Image.open('2787891-571a02494f478229.jpg'))
    image_colors = ImageColorGenerator(background)
    
    #生成词云
    wc = WordCloud(background_color="white", max_words=1000, mask=background, 
               max_font_size=500, random_state=444,font_path='C:\Windows\Fonts\simhei.ttf')
    wc.generate_from_frequencies(dict(keywords))
    plt.imshow(wc.recolor(color_func=image_colors), interpolation='bilinear')
    plt.axis("off")
    plt.show()

def getWordcloud():
    #从数据库获取数据
    data = pd.DataFrame(list(db.get()))
    data = data['comment']
    
    #将所有评论合并
    comments = ''
    for comment in data: 
        comments = comments + comment.strip()
    
    #去除评论中的标点
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    filterdata = re.findall(pattern, comments)
    cleaned_comments = ''.join(filterdata)
    
    #增加停止词
    jieba.analyse.set_stop_words(stop_words_path='chineseStopWords.txt')
    
    #分词
    keywords = jieba.analyse.extract_tags(cleaned_comments, topK=500, withWeight=True, allowPOS=())
    
    #生成词云
    wc = WordCloud(background_color="white", max_words=1000, 
               max_font_size=500, random_state=444,font_path='C:\Windows\Fonts\simhei.ttf')
    wc.generate_from_frequencies(dict(keywords))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()