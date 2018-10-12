import pandas as pd
import json
from pymongo import MongoClient

def __init__(self,collection):
        self.collection=collection
        self.OpenDB()
def OpenDB(self):
        user='******'
        passwd='******'
        host='******'
        port='******'
        auth_db='******'
        uri = "mongodb://"+user+":"+passwd+"@"+host+":"+port+"/"+auth_db+"?authMechanism=SCRAM-SHA-1"
        self.con = MongoClient(uri, connect=False)
        self.db=self.con['wangdong']
        self.collection=self.db[self.collection]
def closeDB(self):
    self.con.close()