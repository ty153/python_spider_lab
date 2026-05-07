import time
import requests
import random
from config import get_headers
import re
import json


def fetch_one(url):
    '''
    请求单个数据
    '''
    res = requests.get(url,headers=get_headers())
    # 解析出数据
    r = re.compile(r'\((?P<name>.*)\)',re.S)
    data_items = json.loads(re.search(r,res.text).group('name'))
    
    data_list = []
    if data_items:
        for item in data_items:
            title=item['title']
            data_list.append({'title':title})
            print('抓取到该数据',title)
            time.sleep(random.uniform(0.1,0.3))
        return data_list
    else:
        print('数据一点没抓取到,请重试')


