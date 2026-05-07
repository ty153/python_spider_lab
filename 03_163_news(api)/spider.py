import time
import requests
import random
from config import get_headers
import re
import json


def fetch_one(url):
    '''
    请求单个数据 解析JSONP接口
    '''
    try:
        # 发送请求
        res = requests.get(url, headers=get_headers())
        
        # 正则提取 JSONP 内容
        r = re.compile(r'\((?P<name>.*)\)', re.S)
        data_items = json.loads(re.search(r, res.text).group('name'))

        # 空数据直接返回空列表
        if not data_items:
            return []

        # 解析数据
        data_list = []
        for item in data_items:
            title = item['title']
            data_list.append({'title': title})
            print('抓取到该数据', title)
            time.sleep(random.uniform(0.1, 0.3))
            
        return data_list

    except Exception as e:
        print('请求失败或解析失败', e)
        return []