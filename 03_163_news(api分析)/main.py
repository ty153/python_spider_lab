from spider import fetch_one
from storage import database_init,save_to_mysql
import time
import random
from config import PAGE_NUMS

def run():
    database_init()
    for i in range(1,PAGE_NUMS):
        if i == 1:
            url = f'https://news.163.com/special/cm_yaowen20200213/?callback=data_callback'
        else:
            url = f'https://news.163.com/special/cm_yaowen20200213_0{i}/?callback=data_callback'
        try:
            print(f'开始抓取数据')
            data_list = fetch_one(url)
            print(f'抓取到 {len(data_list)} 条数据')  
            save_to_mysql(data_list)
            time.sleep(random.randint(1,3))
        except Exception as e:
            print(f'抓取失败：{e}')  #

if __name__ == '__main__':
    run()