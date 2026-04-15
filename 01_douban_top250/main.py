from spider import fetch_one_page
from storage import database_init,save_to_mysql
import time
from config import PAGE_NUMS
import random

def run():
    database_init()
    for page in range(0,PAGE_NUMS):
    # 俩页测试
    # for page in range(0,2):
        try:
            print(f'正在抓取{page+1}页')
            data_list = fetch_one_page(page_num=page)
            save_to_mysql(data_list)
            time.sleep(random.randint(1,3))
        except:
            print(f'抓取失败,跳过第{page+1}页')
            continue

if __name__ == '__main__':
    run()