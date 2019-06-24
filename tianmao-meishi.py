from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import re
import pymongo

driver=webdriver.Chrome()
wd = WebDriverWait(driver, 10)

def seach():
    try:
        driver.get('https://www.taobao.com/')
        input=wd.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#q'))
        )
        submit=wd.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button'))
        )
        input.clear()
        input.send_keys('美食')
        submit.click()
        page_num=wd.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total'))
        )
        get_produce()
        return page_num.text
    except Exception:
        seach()
def write_to_mongo(value):
    # 配置数据库信息
    MONGO_URl = 'localhost'
    MONGO_DB = 'tianmao'  # 数据库名
    MONGO_TABLE = 'meishi'  # 表名

    # 连接数据库
    client = pymongo.MongoClient(MONGO_URl)
    db = client[MONGO_DB]
    try:
        db[MONGO_TABLE].insert(value)
        print('插入数据成功',value)
    except Exception:
        print('插入数据失败',value)

def next_page(page_num):
    try:
        input=wd.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input'))
        )
        button=wd.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )
        input.clear()
        input.send_keys(page_num)
        button.click()
        wd.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_num))
        )
        get_produce()
    except Exception:
        next_page(page_num)
def get_produce():
    wd.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html=driver.page_source
    doc=pq(html)
    items=doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product={
            'image':item.find('.pic .img').attr("src"),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        write_to_mongo(product)
def main():
    total=seach()
    regex=re.compile('(\d+)',re.S)
    num=int(re.findall(regex,total)[0])
    for i in range(2,num+1):
        next_page(i)
    driver.close()


if __name__ == '__main__':
    main()