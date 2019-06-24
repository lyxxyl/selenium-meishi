# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json
import re
from ..items import ZhihuuserItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    def start_requests(self):
        include='data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
        offset=1
        limit=20
        url='https://www.zhihu.com/api/v4/members/penng/followees?include={0}&offset={1}&limit={2}'.format(include,offset*20,limit)
        yield Request(url,callback=self.parse)
    def parse(self, response):
        first_url='https://www.zhihu.com/api/v4/members/{0}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20'
        response=json.loads(response.text)
        if 'data' in response.keys():
            for item in response.get('data'):
                userItem = ZhihuuserItem()
                for field in userItem.fields:
                    if field in item.keys():
                        userItem[field]=item.get(field)
                yield userItem
                yield Request(first_url.format(userItem.get('url_token')))

        if 'paging' in response.keys():
            next=response.get('paging').get('is_end')
            if not next:
                next_url = response.get('paging').get("next")
                regex=re.compile('offset=(\d+)',re.S)
                num=re.findall(regex,next_url)[0]
                regex2=re.compile('https://www.zhihu.com/members/(.*?)/')
                name=re.findall(regex2,next_url)[0]
                base_url='https://www.zhihu.com/api/v4/members/{1}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={0}&limit=20'.format(num,name)
                print(base_url)
                yield Request(base_url,callback=self.parse)
