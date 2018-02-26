# -*- coding: utf-8 -*-
from scrapy import Spider, Request, FormRequest
from lagou.items import LagouItem
from pyquery import PyQuery as pq
import json
import re
from lagou.mongodbutil import MongodbUtil
import time


class LagouSpider(Spider):
    name = 'lagou'
    allow_domains = ['lagou.com']
    # start_urls = ['https://www.lagou.com/']
    url = 'https://www.lagou.com/jobs/positionAjax.json'
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56",
        "Referer": "https://www.lagou.com/jobs/list_?"
    }

    def __init__(self, *args, **kwargs):
        super(LagouSpider, self).__init__()
        self.city = kwargs.pop('city', None)
        self.keyword = kwargs.pop('key', None)

    def start_requests(self):
        login_url = 'http://passport.lagou.com/login/login.html'
        yield Request(login_url, headers=self.headers, meta={'cookiejar': 1}, callback=self.post_login)

    def post_login(self, response):
        html = pq(response.text)
        server_time = html("input[type='hidden']").eq(1).val()
        login_url = 'http://passport.lagou.com/login/login.html?ts={}'.format(server_time)
        form_data = {
            "isValidate": "true",
            "username": "13213181778",
            "password": "71b1531e0259e16a9d8dcaa0b46ce471"
        }
        yield FormRequest(login_url, formdata=form_data, meta={'cookiejar': response.meta['cookiejar']},
                           headers=self.headers, callback=self.get_page)

    def get_page(self, response):
        for page in range(1, 31):
            form_data = {
                "city": self.city,
                # "kd": self.keyword,
                "kd": u"爬虫",
                "pn": str(page),
                'needAddtionalResult': 'False',
                'isSchoolJob': '0'
            }
            yield FormRequest(url=self.url, formdata=form_data, meta={'cookiejar': response.meta['cookiejar']},
                              headers=self.headers, callback=self.get_job_url)

    def get_job_url(self, response):
        base_url = 'https://www.lagou.com/jobs/{}.html'
        page_content = json.loads(response.body)
        if page_content['success']:
            if len(page_content['content']['positionResult']['result']) == 0:
                print("list为空")
                print(page_content)
                return None
            for item in page_content['content']['positionResult']['result']:
                job_page_url = base_url.format(item['positionId'])
                print(job_page_url)
                self.headers['Referer'] = job_page_url
                yield Request(job_page_url, headers=self.headers,
                              meta={'cookiejar': response.meta['cookiejar'], 'url': job_page_url, 'id': item['positionId']},
                              # meta={'url': job_page_url, 'id': item['positionId']},
                              callback=self.parse)
        else:
            print(page_content)

    i = 0
    status = 0

    def parse(self, response):
        print("我执行了!!!!!!!!!!!!!!!!")
        self.i += 1
        print(self.i)
        item = LagouItem()
        if response.status != 200:
            print(response.status)
            self.status = response.status
            item['url'] = response.meta['url']
            item['code'] = self.status
            item['keyword'] = self.keyword
            return item

        html = pq(response.text)
        self.status = response.status
        item['code'] = self.status
        item['keyword'] = self.keyword
        item['id'] = response.meta['id']
        try:
            address_list = html(".work_addr").children()
            address = ""
            for temp in address_list:
                address += temp.text
            item['address'] = address
            item['url'] = response.meta['url']
            item['advantage'] = html(".job-advantage p").text()
            item['company'] = html(".company").text()
            description_list = html(".job_bt p")
            description = str(description_list).replace("<p>", " ").replace("</p>", " ").replace("<br/>", " ")
            item['description'] = description
            job_info = html(".job_request p span")
            item['salary'] = job_info[0].text
            item['location'] = job_info[1].text.replace("/", "")
            item['experience'] = job_info[2].text.replace("/", "")
            item['education'] = job_info[3].text
            item['type'] = job_info[4].text
            item['label'] = html(".position-label li").text()
            item['name'] = html(".job-name").attr('title')
        except Exception as e:
            print(item['url'], e)
        return item

