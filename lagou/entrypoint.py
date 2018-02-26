from scrapy.cmdline import execute

# keys_list = ['python', '挖掘', '爬虫', '数据分析']
execute(['scrapy', 'crawl', 'lagou', '-a', 'city=深圳', '-a', 'key=python'])