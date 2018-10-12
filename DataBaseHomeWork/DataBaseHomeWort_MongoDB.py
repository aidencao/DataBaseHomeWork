import json
import pymongo

DB_ip = '74.82.218.42'#数据库url
DB_port = 27017#数据库端口
DB_name = 'DatabaseHomework'#数据库名
DB_collection = 'Comment'#集合名

#连接
client = pymongo.MongoClient(DB_ip,DB_port)
db = client[DB_name]
myCollect = db[DB_collection]


# 存入数据库
def save(doc):
    try:
        myCollect.insert(doc)
    except Exception:
        print('存储到MongoDb失败', doc)