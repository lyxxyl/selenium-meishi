import requests
import json
import re
from bs4 import BeautifulSoup
import pymongo

def get_html(url,offset,keyword):
    data={
        'offset':offset,
        'keyword':keyword*20,
    }
    response=requests.get(url,params=data)
    return response.text
def get_url(content):
    content=json.loads(content,encoding='ut8-8')
    if content and 'data' in content.keys():
        url_list=[item.get('article_url',None) for item in content['data']]
        return url_list
    print(content.keys())
def get_url_html(url):
    try:
        headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
        }
        response=requests.get(url,headers=headers)
        return response.text
    except Exception:
        return None
def get_detail(content,url):
    soup=BeautifulSoup(content,'lxml')
    title=soup.title.text
    regex=re.compile(' gallery: JSON.parse(.*?),\n',re.S)
    ret=re.findall(regex,content)
    regex2 = re.compile('"url":"(.*?)"', re.S)
    for item in ret:
        item = item.replace('\\', '')
        url_list=re.findall(regex2,item)
        d={}
        for temp in url_list:
            ident=temp[-10:]
            if ident in d.keys():
                d[ident].append(temp)
            else:
                d[ident]=[temp]
        url_list=[i[0] for i in d.values()]
        yield {
            'title':title,
            'url':url,
            'url_list':url_list
        }
def write_to_mongo(value):
    # 配置数据库信息
    MONGO_URl = 'localhost'
    MONGO_DB = 'toutiao'  # 数据库名
    MONGO_TABLE = 'jiepai'  # 表名

    # 连接数据库
    client = pymongo.MongoClient(MONGO_URl)
    db = client[MONGO_DB]
    db[MONGO_TABLE].insert(value)
def main(keyword,offset):
    url='https://www.toutiao.com/api/search/content/?'
    content=get_html(url,offset,keyword)
    url_list=get_url(content)
    for item in url_list:
        if item:
            text=get_url_html(item)
            info=get_detail(text,item)
            for i in info:
                write_to_mongo(i)



if __name__ == '__main__':
    keyword = '街拍'
    for i in range(10):
        main(keyword,i)
