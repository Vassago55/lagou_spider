from lagou.mongodbutil import MongodbUtil
import re
mongo = MongodbUtil(collection='爬虫', db='lagou')
print(mongo.insert({"1":'1'}))

