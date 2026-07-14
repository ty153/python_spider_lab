# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from news_scrapy.storage import database_init,save_to_mysql
class NewsScrapyPipeline:
    def __init__(self):
        # 初始化数据库和表（只执行一次）
        database_init()
        # 用列表收集所有Item
        self.items = []
        self.batch_size = 100  # 每 100 条入库一次
        self.total_success = 0   

    def process_item(self, item, spider):
        # 不立即入库，先收集起来
        self.items.append(dict(item))

        if len(self.items) >= self.batch_size:
            save_to_mysql(self.items)
            self.total_success += len(self.items)
            print(f"已批量存入 {len(self.items)} 条数据")
            self.items.clear()  # 清空列表，准备下一批
        return item

    def close_spider(self,spider):
        if self.items:
            save_to_mysql(self.items)
            self.total_success += len(self.items)
            print(f"已批量存入 {len(self.items)} 条数据")
            self.items.clear()
        print(f"共入库 {self.total_success} 条数据（含跳过的重复数据由 storage.py 统计）")
        
    
        
