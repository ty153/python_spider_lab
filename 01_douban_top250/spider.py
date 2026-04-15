import requests
import time
from config import HEADERS
from lxml import etree
import re
import random

def fetch_one_page(page_num):
   '''
   抓取单页数据
   '''
   url = f'https://movie.douban.com/top250?start={page_num*25}&filter='

   res = requests.get(url,headers=HEADERS)
   data = res.content.decode()
   tree = etree.HTML(data)
   data_list=[]
   li_list = tree.xpath('//ol[@class="grid_view"]/li')
   for li in li_list:
      # 标题
      title = ''.join(li.xpath('./div/div[2]/div[1]/a/span//text()'))
      # 清理空格等
      title = re.sub(r'\s+','',title)
      # 创作人员等
      credits = ''.join(li.xpath('./div/div[2]/div[2]/p[1]//text()'))
      credits = re.sub(r'\s+','',credits)
      # 评价人数
      rating_count = ''.join(li.xpath('./div/div[2]/div[2]/div/span[4]/text()')).strip()
      # 评分
      rating_num = ''.join(li.xpath('./div/div[2]/div[2]/div/span[2]/text()')).strip()
      # 简介
      con = ''.join(li.xpath('./div/div[2]/div[2]/p[2]//text()')).strip()
      if title:
         data_list.append({
            'title': title ,
            'credits':credits,
            'rating_num':rating_num,
            'rating_count':rating_count,
            'con':con
         })
         print('抓取成功这一条数据',title,credits,rating_count,rating_num,con)
         time.sleep(random.uniform(0.1,0.3))
      else:
         print('抓取失败这一条数据')
         continue
   return data_list
         

if __name__ == '__main__':
    fetch_one_page(0)




   



