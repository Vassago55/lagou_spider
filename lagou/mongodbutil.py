# -*- coding: utf-8 -*-
from pymongo import MongoClient
from lagou import settings

MONGODB_HOST = settings.MONGODB_HOST
MONGODB_PORT = settings.MONGODB_PORT
MONGODB_DB = settings.MONGODB_DB

cnx = MongoClient(MONGODB_HOST, MONGODB_PORT)


class MongodbUtil(object):
    def __init__(self, collection, db=MONGODB_DB):
        self.db = cnx[db]
        self.collection = self.db[collection]

    def is_exist(self, item):
        return self.collection.find(item).count()

    def insert(self, item):
        result = self.collection.insert(item)
        return result

    def is_empty(self):
        return self.collection.find({}).count()

    def pop(self):
        data = self.collection.find_one()
        self.delete({'url': data['url']})
        return data['url']

    def delete(self, item):
        return self.collection.delete_one(item)

if __name__ == '__main__':
    MongodbUtil('test').pop()
