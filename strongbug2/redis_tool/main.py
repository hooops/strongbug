# -*- coding: utf-8 -*-
__author__ = 'swing'
import redis
class mains():
    def __init__(self):
        db = redis.Redis(host='localhost', port=6379, db=1)
        self.db=db
    def Set(self,key,value):
        return self.db.set(key,value)
    def Get(self,key):
        return self.db.get(key)
    def Delete(self,key):
        return self.db.delete(key)



