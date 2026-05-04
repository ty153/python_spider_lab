from spider import crawl_news
from storage import database_init,save_to_mysql
import time
import random

def run():
    database_init()
    try:
        print(f'正在抓取数据')
        data_list = crawl_news()
        print(f'抓取到 {len(data_list)} 条数据')  
        save_to_mysql(data_list)
    except Exception as e:
        print(f'抓取失败：{e}')  #

if __name__ == '__main__':
    run()